import os
import subprocess
import signal
import threading
import time
import sys
import platform

class ServerManager:
    """Manages the FastHTML server process."""
    
    def __init__(self, log_callback=None):
        self.process = None
        self.is_running = False
        self.log_callback = log_callback
        self.log_thread = None
        self.stop_log = False
        
        # Get the project root path
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        
    def start_server(self, port=5004):
        """Start the FastHTML server on the specified port."""
        if self.is_running:
            return
        
        # Activate virtual environment and start server
        is_windows = platform.system() == "Windows"
        
        if is_windows:
            # Windows approach - use a script file
            script_path = os.path.join(self.project_root, "run_server.bat")
            with open(script_path, "w") as f:
                f.write(f"@echo off\n")
                f.write(f"call {os.path.join(self.project_root, 'venv', 'Scripts', 'activate.bat')}\n")
                f.write(f"cd {self.project_root}\n")
                f.write(f"set FASTHTML_PORT={port}\n")
                f.write(f"python main.py\n")
            
            # Run the script
            self.process = subprocess.Popen(
                script_path,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
            )
        else:
            # Unix approach - use a shell script
            script_path = os.path.join(self.project_root, "run_server.sh")
            with open(script_path, "w") as f:
                f.write("#!/bin/bash\n")
                f.write(f"source {os.path.join(self.project_root, 'venv', 'bin', 'activate')}\n")
                f.write(f"cd {self.project_root}\n")
                f.write(f"export FASTHTML_PORT={port}\n")
                f.write(f"python3 main.py\n")
            
            # Make script executable
            os.chmod(script_path, 0o755)
            
            # Run the script in a new process group
            self.process = subprocess.Popen(
                script_path,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                preexec_fn=os.setsid  # Create a new process group
            )
        
        # Start log reading thread
        self.stop_log = False
        self.log_thread = threading.Thread(target=self._read_logs)
        self.log_thread.daemon = True
        self.log_thread.start()
        
        # Mark as running after a brief delay to allow server to start
        time.sleep(2)  
        self.is_running = True
        if self.log_callback:
            self.log_callback(f"Server started on port {port}")
        
    def stop_server(self):
        """Stop the running FastHTML server."""
        if not self.is_running:
            return
        
        # Stop log thread
        self.stop_log = True
        
        try:
            # Terminate the server process
            if self.process:
                if platform.system() == "Windows":
                    # Windows - send CTRL+BREAK to the process group
                    os.kill(self.process.pid, signal.CTRL_BREAK_EVENT)
                else:
                    # Unix - send SIGTERM to the process group
                    try:
                        pgid = os.getpgid(self.process.pid)
                        os.killpg(pgid, signal.SIGTERM)
                    except Exception as e:
                        if self.log_callback:
                            self.log_callback(f"Error sending SIGTERM: {str(e)}")
                        # Fall back to terminate
                        self.process.terminate()
                
                # Wait for the process to exit
                try:
                    self.process.communicate(timeout=5)
                except subprocess.TimeoutExpired:
                    # Force kill if needed
                    if platform.system() == "Windows":
                        subprocess.run(f"taskkill /F /T /PID {self.process.pid}", shell=True)
                    else:
                        try:
                            pgid = os.getpgid(self.process.pid)
                            os.killpg(pgid, signal.SIGKILL)
                        except:
                            pass
        except Exception as e:
            if self.log_callback:
                self.log_callback(f"Error stopping server: {str(e)}")
        
        # Clean up the process
        self.process = None
        self.is_running = False
        
        # Clean up script files
        try:
            if platform.system() == "Windows":
                if os.path.exists(os.path.join(self.project_root, "run_server.bat")):
                    os.remove(os.path.join(self.project_root, "run_server.bat"))
            else:
                if os.path.exists(os.path.join(self.project_root, "run_server.sh")):
                    os.remove(os.path.join(self.project_root, "run_server.sh"))
        except:
            pass
            
        if self.log_callback:
            self.log_callback("Server stopped")
    
    def check_status(self):
        """Check if the server is still running."""
        if not self.process:
            return False
            
        # Check if process is still running
        return self.process.poll() is None
    
    def _read_logs(self):
        """Read logs from the server process and pass them to the callback."""
        if not self.process:
            return
            
        while not self.stop_log:
            try:
                line = self.process.stdout.readline()
                if not line:
                    # End of output - process might have terminated
                    if self.process.poll() is not None:
                        break
                    time.sleep(0.1)  # Avoid spinning the CPU
                    continue
                    
                if self.log_callback:
                    self.log_callback(line.strip())
            except Exception as e:
                if self.log_callback:
                    self.log_callback(f"Error reading logs: {str(e)}")
                break
                
        # Process ended
        if self.process and self.process.poll() is not None:
            self.is_running = False 