#!/usr/bin/env python3
import os
import sys
import subprocess
import webbrowser
import tkinter as tk
from tkinter import messagebox
import signal
import time

class RadioNulaLauncher:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Radio NULA Search")
        
        # Set window size and position
        window_width = 300
        window_height = 150
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Make window stay on top
        self.root.attributes('-topmost', True)
        
        # Status label
        self.status_label = tk.Label(self.root, text="Server: Stopped", font=('Arial', 12))
        self.status_label.pack(pady=10)
        
        # Start button
        self.start_button = tk.Button(self.root, text="Start Server", command=self.start_server,
                                    bg='#4CAF50', fg='white', font=('Arial', 12))
        self.start_button.pack(pady=5)
        
        # Stop button
        self.stop_button = tk.Button(self.root, text="Stop Server", command=self.stop_server,
                                   bg='#f44336', fg='white', font=('Arial', 12), state='disabled')
        self.stop_button.pack(pady=5)
        
        # Open Browser button
        self.browser_button = tk.Button(self.root, text="Open in Browser", command=self.open_browser,
                                      bg='#2196F3', fg='white', font=('Arial', 12), state='disabled')
        self.browser_button.pack(pady=5)
        
        self.process = None
        self.server_running = False

    def activate_venv(self):
        """Ensure we're running in the virtual environment"""
        if 'VIRTUAL_ENV' not in os.environ:
            venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv')
            if sys.platform == 'win32':
                python_path = os.path.join(venv_path, 'Scripts', 'python.exe')
            else:
                python_path = os.path.join(venv_path, 'bin', 'python3')
            
            if not os.path.exists(python_path):
                messagebox.showerror("Error", "Virtual environment not found. Please run setup first.")
                sys.exit(1)
            
            # Restart the script with the virtual environment Python
            os.execv(python_path, [python_path] + sys.argv)

    def start_server(self):
        """Start the server process"""
        try:
            # First, try to stop any existing server
            subprocess.run([sys.executable, 'run.py', 'stop'], 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
            
            self.process = subprocess.Popen(
                [sys.executable, 'run.py', 'start'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait a bit for the server to start
            time.sleep(2)
            
            # Check if server started successfully
            if self.process.poll() is None:
                self.server_running = True
                self.status_label.config(text="Server: Running")
                self.start_button.config(state='disabled')
                self.stop_button.config(state='normal')
                self.browser_button.config(state='normal')
                
                # Wait a bit more before opening browser
                self.root.after(1000, self.open_browser)
            else:
                stdout, stderr = self.process.communicate()
                error_msg = stderr.decode() if stderr else "Unknown error"
                messagebox.showerror("Error", f"Failed to start server:\n{error_msg}")
                self.stop_server()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start server: {str(e)}")
            self.stop_server()

    def stop_server(self):
        """Stop the server process"""
        if self.process:
            try:
                # Try to stop gracefully first
                subprocess.run([sys.executable, 'run.py', 'stop'])
                
                # If process is still running, terminate it
                if self.process.poll() is None:
                    self.process.terminate()
                    time.sleep(1)
                    if self.process.poll() is None:
                        self.process.kill()
            except:
                pass
            
            self.process = None
            
        self.server_running = False
        self.status_label.config(text="Server: Stopped")
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.browser_button.config(state='disabled')

    def open_browser(self):
        """Open the application in the default web browser"""
        webbrowser.open('http://localhost:5001')

    def on_closing(self):
        """Handle window closing"""
        if self.server_running:
            if messagebox.askokcancel("Quit", "The server is running. Do you want to stop it and quit?"):
                self.stop_server()
                self.root.destroy()
        else:
            self.root.destroy()

    def run(self):
        """Start the GUI application"""
        self.activate_venv()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

if __name__ == "__main__":
    app = RadioNulaLauncher()
    app.run() 