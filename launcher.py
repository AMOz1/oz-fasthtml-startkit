import os
import sys
import tkinter as tk
from tkinter import ttk, scrolledtext
import webbrowser
import threading
from server_manager import ServerManager

class FastHTMLLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("FastHTML Launcher")
        self.root.geometry("260x260")  # Smaller window size
        self.root.resizable(True, True)
        
        # Set custom button styles
        self.setup_styles()
        
        # Server configuration
        self.port = 5004
        self.server_manager = ServerManager(log_callback=self.update_logs)
        
        # Initialize UI elements that might be referenced before creation
        self.start_stop_button = None
        self.open_browser_button = None
        self.status_canvas = None
        self.log_text = None
        
        # Create UI
        self.setup_ui()
        
        # Start monitoring thread
        self.monitoring = True
        self.last_status = False  # Track previous status
        self.monitor_thread = threading.Thread(target=self.monitor_server)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()
        
        # Bind close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def setup_styles(self):
        """Set up custom styles for the buttons"""
        style = ttk.Style()
        
        # Blue style for Start Server and Apply buttons
        style.configure("Blue.TButton", 
                        background="#3498db", 
                        foreground="white")
        
        # Red style for Stop Server button
        style.configure("Red.TButton", 
                        background="#e74c3c", 
                        foreground="white")
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status frame
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(status_frame, text="Server Status:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.status_canvas = tk.Canvas(status_frame, width=20, height=20)
        self.status_canvas.pack(side=tk.LEFT)
        
        # Controls frame
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill=tk.X, pady=10)
        
        # Start/Stop button with blue style (will be changed to red when server running)
        self.start_stop_button = ttk.Button(
            controls_frame, 
            text="Start Server",
            style="Blue.TButton",
            command=self.toggle_server
        )
        self.start_stop_button.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        # Open in Browser button
        self.open_browser_button = ttk.Button(
            controls_frame, 
            text="Open in Browser", 
            command=self.open_browser,
            state="disabled"
        )
        self.open_browser_button.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Now that all UI elements are created, we can update the status
        self.update_status_indicator(False)
        
        # Port configuration
        port_frame = ttk.Frame(main_frame)
        port_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(port_frame, text="Port:").pack(side=tk.LEFT, padx=(0, 10))
        
        self.port_var = tk.StringVar(value=str(self.port))
        port_entry = ttk.Entry(port_frame, textvariable=self.port_var, width=8)
        port_entry.pack(side=tk.LEFT, padx=(0, 10))
        
        # Apply button with blue style
        apply_port_button = ttk.Button(
            port_frame,
            text="Apply",
            style="Blue.TButton",
            command=self.apply_port
        )
        apply_port_button.pack(side=tk.LEFT)
        
        # Log section - smaller to fit window size
        log_frame = ttk.LabelFrame(main_frame, text="Server Logs")
        log_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=5)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_text.config(state=tk.DISABLED)
        
        # Add some instructions
        self.update_logs("Welcome to FastHTML Launcher!")
        self.update_logs("Click 'Start Server' to launch your application.")
        self.update_logs("Current port: " + str(self.port))
    
    def update_status_indicator(self, is_running):
        if not self.status_canvas or not self.start_stop_button or not self.open_browser_button:
            return  # UI elements not created yet
            
        self.status_canvas.delete("all")
        color = "#4CAF50" if is_running else "#F44336"  # Green if running, red if stopped
        self.status_canvas.create_oval(2, 2, 18, 18, fill=color, outline="")
        
        # Update button text and style
        if is_running:
            self.start_stop_button.config(text="Stop Server", style="Red.TButton")
        else:
            self.start_stop_button.config(text="Start Server", style="Blue.TButton")
        
        # Update browser button state
        state = "normal" if is_running else "disabled"
        self.open_browser_button.config(state=state)
    
    def toggle_server(self):
        if self.server_manager.is_running:
            self.update_logs("Stopping server...")
            self.server_manager.stop_server()
            self.update_status_indicator(False)  # Update UI immediately
        else:
            try:
                port = int(self.port_var.get())
                self.port = port
                
                # Create a new thread to start the server to avoid freezing the UI
                threading.Thread(
                    target=self.server_manager.start_server,
                    args=(port,),
                    daemon=True
                ).start()
                
                self.update_logs(f"Starting server on port {port}...")
                
                # Update UI to show "stopping" state
                self.update_status_indicator(True)
            except ValueError:
                self.update_logs("Invalid port number")
                self.port_var.set(str(self.port))
    
    def apply_port(self):
        try:
            new_port = int(self.port_var.get())
            
            # Only update if the server is not running
            if not self.server_manager.is_running:
                self.port = new_port
                self.update_logs(f"Port set to {self.port}")
            else:
                self.update_logs("Cannot change port while server is running")
                self.port_var.set(str(self.port))
        except ValueError:
            self.update_logs("Invalid port number")
            self.port_var.set(str(self.port))
    
    def open_browser(self):
        url = f"http://localhost:{self.port}"
        webbrowser.open(url)
        self.update_logs(f"Opening {url} in browser")
    
    def update_logs(self, message):
        if not self.log_text:
            print(message)  # Fallback if log_text not created yet
            return
            
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def monitor_server(self):
        """Periodically check server status and update UI."""
        while self.monitoring:
            try:
                is_running = self.server_manager.check_status()
                
                # Only update the UI if the status has changed
                if is_running != self.last_status:
                    # Update UI in a thread-safe way
                    self.root.after(0, lambda r=is_running: self.update_status_indicator(r))
                    self.last_status = is_running
                    
                    # Log status changes
                    if is_running:
                        self.root.after(0, lambda: self.update_logs("Server is running"))
                    else:
                        self.root.after(0, lambda: self.update_logs("Server is stopped"))
            except Exception as e:
                print(f"Error in monitoring thread: {str(e)}")
                
            # Sleep to avoid excessive CPU usage
            try:
                threading.Event().wait(1.0)
            except:
                break
    
    def on_close(self):
        """Handle window close event."""
        self.monitoring = False
        if self.server_manager.is_running:
            self.update_logs("Stopping server before exit...")
            self.server_manager.stop_server()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = FastHTMLLauncher(root)
    root.mainloop()

if __name__ == "__main__":
    main() 