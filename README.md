# FastHTML Project Starter Kit

A modern web application starter kit built with the FastHTML framework and a convenient GUI launcher. This project provides everything you need to get started with FastHTML development quickly and efficiently.

![FastHTML Launcher](https://github.com/USER_NAME/oz-fasthtml-startkit/assets/YOUR_ASSET_ID/launcher-screenshot.png)

## About This Project

This starter kit includes:

1. **FastHTML Application** - A simple but feature-rich web application showcasing key FastHTML features
2. **GUI Launcher** - A desktop application for starting, stopping, and managing your FastHTML server
3. **Complete Setup Scripts** - Everything needed to get up and running with minimal effort
4. **Pico CSS Component Library** - A comprehensive example of Pico CSS components implemented in FastHTML

## Features

### FastHTML Demo Application

- **Interactive Components** - Counter and message board demonstrating HTMX functionality
- **Clean Structure** - Well-organized code following FastHTML best practices
- **CSS Styling** - Responsive design with custom styling
- **HTMX Integration** - Demonstrates dynamic content updates without page reloads

### GUI Launcher Application

- **Server Management** - Start and stop your FastHTML server with a single click
- **Status Monitoring** - Real-time status indicators and logging
- **Port Configuration** - Easily change server ports
- **Browser Integration** - Open your application in a browser directly from the launcher

## Getting Started

### Installation

#### Option 1: Clone the Repository

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/oz-fasthtml-startkit.git

# Navigate to the project directory
cd oz-fasthtml-startkit
```

#### Option 2: Download as ZIP

1. Click the **Code** button above
2. Select **Download ZIP**
3. Extract the ZIP file to your preferred location

### Running the Application

#### Quick Start

The fastest way to get started is by using the launcher:

1. **Double-click the `run_launcher.command` file** (Mac) or `run_launcher.bat` file (Windows)
2. **Click "Start Server"** in the launcher
3. **Click "Open in Browser"** to view your application

That's it! The launcher will handle virtual environment setup, dependencies, and server management for you. By default, the application will run on port 5004.

#### Manual Setup

If you prefer setting up manually:

1. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   ```

2. **Activate the virtual environment**:
   - macOS/Linux: `source venv/bin/activate`
   - Windows: `venv\Scripts\activate`

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python3 main.py
   ```

5. **Open your browser** at http://localhost:5004

## Project Structure

```
fasthtml-project/
├── main.py                 # Main FastHTML application
├── example.py              # Pico CSS component examples
├── requirements.txt        # Python dependencies
├── static/                 # Static assets
│   ├── style.css           # CSS styling
│   └── pico.css            # Custom Pico CSS
├── example/                # Original HTML examples
│   └── img/                # Example images
├── launcher.py             # GUI launcher application
├── server_manager.py       # Server management backend
├── run_launcher.command    # macOS launcher script
├── run_launcher.bat        # Windows launcher script
├── .gitignore              # Git ignore file
└── README.md               # Project documentation
```

## Understanding the Code

### FastHTML Application (`main.py`)

The main application is built using FastHTML's declarative syntax and HTMX integration:

```python
@rt('/')
def get():
    return Titled(
        "FastHTML Demo",
        P('Hello World!', hx_get="/change"),
        Div(
            P(f"Counter: {counter}"),
            Button("Increment", hx_post="/increment", hx_target="#counter"),
            id="counter"
        ),
        # More components...
    )
```

Key features demonstrated:
- Route declaration with `@rt` decorators
- HTML generation with Python functions
- HTMX attributes for interactivity (`hx_get`, `hx_post`, `hx_target`)
- Component composition and nesting
- Server-side state management

### GUI Launcher

The launcher is built with Tkinter and provides:
- Visual feedback on server status
- Start/stop controls
- Port configuration
- Log display
- Browser integration

## Customizing Your Project

### Modifying the FastHTML Application

1. Edit `main.py` to add routes and functionality
2. Update `static/style.css` for styling changes
3. Add additional static files as needed

### Customizing CSS Styling

This starter kit includes the ability to use a custom version of Pico CSS:

#### Using the Built-in Theme Switcher

The application comes with a theme switcher that allows you to toggle between:
- Default Pico CSS (from CDN)
- Custom Pico CSS (from `static/pico.css`)

To use this feature:
1. Simply select your preferred theme from the dropdown at the top of the page
2. Your selection will be saved in localStorage and remembered between visits

#### Modifying the Custom Pico CSS

To customize the Pico CSS:
1. Edit the `static/pico.css` file to match your design needs
2. Reload the application to see your changes
3. The custom theme will be automatically selected for new visitors

#### Pico CSS Component Examples

This starter kit includes a comprehensive Pico CSS component example that serves as a visual reference and code example for building UI components:

1. **Run the example application:**
   ```bash
   source venv/bin/activate
   python example.py
   ```

2. **Open your browser** to http://localhost:5004

3. **Explore the components** - The example showcases all standard Pico CSS components including:
   - Typography elements
   - Form controls
   - Buttons
   - Tables
   - Modals
   - Accordions
   - Cards
   - Theme switching

4. **Learn from the source code** - Examine `example.py` to see how HTML structures are converted to FastHTML's declarative syntax. It demonstrates:
   - How to structure complex layouts
   - Working with JavaScript in FastHTML
   - Custom font integration
   - Component nesting patterns
   - Browser feature detection

Additional details can be found in the `example/README.md` file.

#### Disabling the Theme Switcher

If you want to use only your custom Pico CSS:
1. Edit `main.py` and remove the theme switcher HTML elements
2. Modify the CSS header section to only include your custom CSS:
   ```python
   app.hdrs += (
       Link(rel="stylesheet", href="/static/pico.css"),
       Link(rel="stylesheet", href="/static/style.css"),
   )
   ```

### Extending the Launcher

If you need to customize the launcher:
1. Edit `launcher.py` for UI changes
2. Modify `server_manager.py` to change server behavior

## Advanced Usage

### Environment Variables

The application uses the following environment variables:
- `FASTHTML_PORT` - The port to run the server on (default: 5004)

### Using Custom Ports

You can change the port in two ways:
1. Through the launcher UI
2. By setting the `FASTHTML_PORT` environment variable before starting the application

### Creating a macOS Application Bundle

To create a standalone macOS application:

1. Install required tools:
   ```bash
   pip install py2app
   ```

2. Create a setup.py file with:
   ```python
   from setuptools import setup
   APP = ['launcher.py']
   OPTIONS = {
       'argv_emulation': True,
       'packages': ['tkinter'],
       'includes': ['webbrowser', 'threading'],
   }
   setup(
       app=APP,
       options={'py2app': OPTIONS},
       setup_requires=['py2app'],
   )
   ```

3. Build the application:
   ```bash
   python setup.py py2app
   ```

## Resources

- [FastHTML Documentation](https://fastht.ml/docs/)
- [HTMX Documentation](https://htmx.org/)
- [Tkinter Documentation](https://docs.python.org/3/library/tkinter.html)

## Troubleshooting

### Common Issues

- **"Module not found" errors**: Make sure your virtual environment is activated
- **Port conflicts**: Change the port through the launcher if you see "Address already in use"
- **Launcher startup issues**: Ensure you have Python 3.7+ and Tkinter installed

## Contributing

Contributions to improve this starter kit are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## License

This project is open source and available under the MIT License. 