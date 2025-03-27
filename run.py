#!/usr/bin/env python3
import os
import sys
import signal
import subprocess
import socket
import time
import psutil

def kill_python_on_port(port):
    """Kill any Python process using the specified port"""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            if proc.info['name'] == 'Python' or proc.info['name'] == 'python3':
                for conn in proc.connections():
                    if conn.laddr.port == port:
                        os.kill(proc.info['pid'], signal.SIGTERM)
                        time.sleep(1)  # Give it time to die
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

def is_port_in_use(port):
    """Check if a port is in use"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('localhost', port))
            return False
        except socket.error:
            return True

def kill_server(pid_file):
    """Kill the server if it's running"""
    if os.path.exists(pid_file):
        with open(pid_file, 'r') as f:
            try:
                pid = int(f.read().strip())
                os.kill(pid, signal.SIGTERM)
                print(f"Stopped server with PID {pid}")
            except (ProcessLookupError, ValueError):
                pass
        os.remove(pid_file)

def clean_environment():
    """Clean up the environment before starting"""
    port = 5001
    pid_file = '.server.pid'
    
    # Kill any process using our port
    kill_python_on_port(port)
    
    # Remove PID file if it exists
    if os.path.exists(pid_file):
        os.remove(pid_file)
    
    # Remove old template files
    if os.path.exists('templates'):
        for file in os.listdir('templates'):
            os.remove(os.path.join('templates', file))
        os.rmdir('templates')

def start_server():
    """Start the server"""
    port = 5001
    pid_file = '.server.pid'

    # Clean up environment
    clean_environment()

    # Start the server
    print("Starting server...")
    process = subprocess.Popen(
        ['python3', 'app.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    # Save the PID
    with open(pid_file, 'w') as f:
        f.write(str(process.pid))

    # Wait a bit to ensure server starts
    time.sleep(2)

    if is_port_in_use(port):
        print(f"Server running at http://localhost:{port}")
        print("Press Ctrl+C to stop")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            kill_server(pid_file)
            print("\nServer stopped")
    else:
        print("Failed to start server")

def stop_server():
    """Stop the server"""
    clean_environment()
    print("Server stopped")

def show_help():
    """Show help message"""
    print("\nUsage:")
    print("  python3 run.py [command]")
    print("\nCommands:")
    print("  start  - Start the server")
    print("  stop   - Stop the server")
    print("  help   - Show this help message")

if __name__ == "__main__":
    # Ensure virtual environment is activated
    if 'VIRTUAL_ENV' not in os.environ:
        print("Virtual environment not activated. Please run:")
        print("source venv/bin/activate")
        sys.exit(1)

    if len(sys.argv) != 2:
        show_help()
        sys.exit(1)

    command = sys.argv[1]

    if command == "help":
        show_help()
    elif command == "start":
        start_server()
    elif command == "stop":
        stop_server()
    else:
        show_help() 