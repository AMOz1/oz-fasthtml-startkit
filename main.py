# pylint: disable=undefined-variable
# pyright: reportUndefinedVariable=false
from fasthtml.common import *
import os

# Initialize the application and router with both CSS options available
app, rt = fast_app(pico=False)  # Disable default Pico CSS

# A simple counter to demonstrate state
counter = 0
messages = []

@rt('/')
def get():
    return Titled(
        "FastHTML Demo",
        Div(
            Div(
                Label("Theme: ", fr="theme-select"),
                Select(
                    Option("Default Pico", value="default"),
                    Option("Custom Pico", value="custom"),
                    id="theme-select"
                ),
                class_="theme-switcher"
            ),
            P('Hello World!', hx_get="/change"),
            Div(
                P(f"Counter: {counter}"),
                Button("Increment", hx_post="/increment", hx_target="#counter"),
                id="counter"
            ),
            Div(
                H2("Message Board"),
                Form(
                    Input(type="text", name="message", placeholder="Enter a message"),
                    Button("Submit", type="submit"),
                    hx_post="/add-message",
                    hx_target="#messages"
                ),
                Div(
                    [P(msg) for msg in messages],
                    id="messages"
                )
            )
        )
    )

@rt('/change')
def get():
    return P('Nice to be here!')

@rt('/increment', methods=['POST'])
def post():
    global counter
    counter += 1
    return Div(
        P(f"Counter: {counter}"),
        Button("Increment", hx_post="/increment", hx_target="#counter"),
        id="counter"
    )

@rt('/add-message', methods=['POST'])
def post():
    global messages
    message = request.form.get('message', '').strip()
    if message:
        messages.append(message)
    return Div(
        [P(msg) for msg in messages],
        id="messages"
    )

@rt('/static/<path:path>')
def get(path):
    return send_from_directory('static', path)

# Add CSS styling with custom headers
app.hdrs += (
    # Default Pico CSS (CDN version)
    Link(rel="stylesheet", href="https://unpkg.com/@picocss/pico@1.5.10/css/pico.min.css", id="pico-css"),
    # Custom Pico CSS
    Link(rel="stylesheet", href="/static/pico.css", id="custom-pico-css"),
    # Additional custom styles
    Link(rel="stylesheet", href="/static/style.css"),
    # Theme switcher script
    Script(src="/static/theme-switcher.js"),
)

# Get port from environment variable if set
port = int(os.environ.get('FASTHTML_PORT', 5004))

# Start the server
print(f"Starting FastHTML server. Visit http://localhost:{port} to see your application.")
serve(port=port) 