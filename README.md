# Radio NULA Track Search

A simple search application for the Radio NULA SQLite database, built with FastAPI and HTMX to provide a modern, dynamic search experience.

## Prerequisites

- Python 3.x
- `radio.db` SQLite database file in the project root

## Initial Setup

1. Create and activate a virtual environment:
```bash
# Create virtual environment
python3 -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
.\venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### Option 1: Using the Desktop Launcher (Recommended for macOS)

Simply double-click the `start_app.command` file. This will:
- Open a control window with buttons to manage the server
- Start the server automatically
- Open your web browser when ready
- Allow you to stop the server when done

If this is the first time running the launcher, macOS might show a security warning. To fix this:
1. Right-click (or Control-click) on `start_app.command`
2. Choose "Open" from the menu
3. Click "Open" in the security dialog
After doing this once, you can double-click the file normally.

### Option 2: Using the Command Line

We provide a server management script for command-line users:

```bash
# Make sure your virtual environment is activated
source venv/bin/activate

# Start the server
python3 run.py start

# Stop the server
python3 run.py stop

# Show help
python3 run.py help
```

The script will:
- Clean up any existing server instances
- Start the server on port 5001
- Show the server URL (http://localhost:5001)
- Handle server shutdown gracefully when you press Ctrl+C

## Features

- Search through tracks in the database
- Live search as you type
- Case-insensitive search
- Multi-word search (finds tracks containing ALL words)
- Clean, responsive UI with DaisyUI and Tailwind CSS
- Mobile-friendly design
- Easy-to-use desktop launcher

## Implementation Details

### Database Structure
The application expects a SQLite database named `radio.db` with a table named `tracks` containing a column `track`.

### Search Logic
- Splits search query into words
- Matches all words (AND logic)
- Case-insensitive matching
- Results sorted alphabetically

### Technical Stack
- FastAPI - Modern, fast web framework
- HTMX - Dynamic updates without JavaScript
- DaisyUI/Tailwind CSS - Responsive styling
- SQLite - Lightweight database
- Jinja2 - Template rendering
- Uvicorn - ASGI server
- Tkinter - GUI launcher

## Troubleshooting

If you can't access the server:

1. Make sure no other application is using port 5001
2. Use the launcher's "Stop Server" button, then click "Start Server" again
3. If using command line:
   ```bash
   python3 run.py stop
   python3 run.py start
   ```

4. If you see "Module not found" errors:
   ```bash
   # Reactivate your virtual environment
   source venv/bin/activate
   # Reinstall dependencies
   pip install -r requirements.txt
   ```

5. If the launcher doesn't open:
   - Right-click `start_app.command` and choose "Open"
   - Click "Open" in the security dialog
   - Try double-clicking again