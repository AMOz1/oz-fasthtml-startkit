# pylint: disable=undefined-variable
# pyright: reportUndefinedVariable=false
from fasthtml.common import *
import os

# Initialize the application and router without default Pico CSS
app, rt = fast_app(pico=False)

# Theme switcher JavaScript
theme_switcher_js = """
/*!
 * Minimal theme switcher
 *
 * Pico.css - https://picocss.com
 * Copyright 2019-2024 - Licensed under MIT
 */

const themeSwitcher = {
  // Config
  _scheme: "auto",
  menuTarget: "details.dropdown",
  buttonsTarget: "a[data-theme-switcher]",
  buttonAttribute: "data-theme-switcher",
  rootAttribute: "data-theme",
  localStorageKey: "picoPreferredColorScheme",

  // Init
  init() {
    this.scheme = this.schemeFromLocalStorage;
    this.initSwitchers();
  },

  // Get color scheme from local storage
  get schemeFromLocalStorage() {
    return window.localStorage?.getItem(this.localStorageKey) ?? this._scheme;
  },

  // Preferred color scheme
  get preferredColorScheme() {
    return window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
  },

  // Init switchers
  initSwitchers() {
    const buttons = document.querySelectorAll(this.buttonsTarget);
    buttons.forEach((button) => {
      button.addEventListener(
        "click",
        (event) => {
          event.preventDefault();
          // Set scheme
          this.scheme = button.getAttribute(this.buttonAttribute);
          // Close dropdown
          document.querySelector(this.menuTarget)?.removeAttribute("open");
        },
        false
      );
    });
  },

  // Set scheme
  set scheme(scheme) {
    if (scheme == "auto") {
      this._scheme = this.preferredColorScheme;
    } else if (scheme == "dark" || scheme == "light") {
      this._scheme = scheme;
    }
    this.applyScheme();
    this.schemeToLocalStorage();
  },

  // Get scheme
  get scheme() {
    return this._scheme;
  },

  // Apply scheme
  applyScheme() {
    document.querySelector("html")?.setAttribute(this.rootAttribute, this.scheme);
  },

  // Store scheme to local storage
  schemeToLocalStorage() {
    window.localStorage?.setItem(this.localStorageKey, this.scheme);
  },
};

// Init
themeSwitcher.init();
"""

# Modal JavaScript
modal_js = """
/*
 * Modal
 *
 * Pico.css - https://picocss.com
 * Copyright 2019-2024 - Licensed under MIT
 */

// Config
const isOpenClass = "modal-is-open";
const openingClass = "modal-is-opening";
const closingClass = "modal-is-closing";
const scrollbarWidthCssVar = "--pico-scrollbar-width";
const animationDuration = 400; // ms
let visibleModal = null;

// Toggle modal
const toggleModal = (event) => {
  event.preventDefault();
  const modal = document.getElementById(event.currentTarget.dataset.target);
  if (!modal) return;
  modal && (modal.open ? closeModal(modal) : openModal(modal));
};

// Open modal
const openModal = (modal) => {
  const { documentElement: html } = document;
  const scrollbarWidth = getScrollbarWidth();
  if (scrollbarWidth) {
    html.style.setProperty(scrollbarWidthCssVar, `${scrollbarWidth}px`);
  }
  html.classList.add(isOpenClass, openingClass);
  setTimeout(() => {
    visibleModal = modal;
    html.classList.remove(openingClass);
  }, animationDuration);
  modal.showModal();
};

// Close modal
const closeModal = (modal) => {
  visibleModal = null;
  const { documentElement: html } = document;
  html.classList.add(closingClass);
  setTimeout(() => {
    html.classList.remove(closingClass, isOpenClass);
    html.style.removeProperty(scrollbarWidthCssVar);
    modal.close();
  }, animationDuration);
};

// Close with a click outside
document.addEventListener("click", (event) => {
  if (visibleModal === null) return;
  const modalContent = visibleModal.querySelector("article");
  const isClickInside = modalContent.contains(event.target);
  !isClickInside && closeModal(visibleModal);
});

// Close with Esc key
document.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && visibleModal) {
    closeModal(visibleModal);
  }
});

// Get scrollbar width
const getScrollbarWidth = () => {
  const scrollbarWidth = window.innerWidth - document.documentElement.clientWidth;
  return scrollbarWidth;
};

// Is scrollbar visible
const isScrollbarVisible = () => {
  return document.body.scrollHeight > screen.height;
};
"""

# Font styles
font_style = """
:root {
  --oz-pico-font-family-sans-serif: 'Source Sans 3', system-ui, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, Helvetica, Arial, "Helvetica Neue", sans-serif, var(--oz-pico-font-family-emoji);
  --oz-pico-font-family: var(--oz-pico-font-family-sans-serif);
}
"""

@rt('/')
def get():
    return Titled(
        "Preview • Pico CSS",  # Page title
        
        # Header
        Div(
            Div(
                H1("Pico"),
                P("A pure HTML example, without dependencies."),
                class_="hgroup"
            ),
            Nav(
                Ul(
                    Li(
                        Details(
                            Summary("Theme", role="button", class_="secondary"),
                            Ul(
                                Li(A("Auto", href="#", **{"data-theme-switcher": "auto"})),
                                Li(A("Light", href="#", **{"data-theme-switcher": "light"})),
                                Li(A("Dark", href="#", **{"data-theme-switcher": "dark"}))
                            ),
                            class_="dropdown"
                        )
                    )
                )
            ),
            class_="container"
        ),
        
        # Main content
        Main(
            # Preview section
            Section(
                H2("Preview"),
                P("Sed ultricies dolor non ante vulputate hendrerit. Vivamus sit amet suscipit sapien. Nulla iaculis eros a elit pharetra egestas."),
                Form(
                    Div(
                        Input(type="text", name="firstname", placeholder="First name", **{"aria-label": "First name"}, required=True),
                        Input(type="email", name="email", placeholder="Email address", **{"aria-label": "Email address"}, autocomplete="email", required=True),
                        Button("Subscribe", type="submit"),
                        class_="grid"
                    ),
                    Fieldset(
                        Label(
                            Input(type="checkbox", role="switch", id="terms", name="terms"),
                            " I agree to the ",
                            A("Privacy Policy", href="#", onclick="event.preventDefault()")
                        )
                    )
                ),
                id="preview"
            ),
            
            # Typography section
            Section(
                H2("Typography"),
                P("Aliquam lobortis vitae nibh nec rhoncus. Morbi mattis neque eget efficitur feugiat. Vivamus porta nunc a erat mattis, mattis feugiat turpis pretium. Quisque sed tristique felis."),
                
                # Blockquote
                Blockquote(
                    '"Maecenas vehicula metus tellus, vitae congue turpis hendrerit non. Nam at dui sit amet ipsum cursus ornare."',
                    Footer(
                        Cite("- Phasellus eget lacinia")
                    )
                ),
                
                # Lists
                H3("Lists"),
                Ul(
                    Li("Aliquam lobortis lacus eu libero ornare facilisis."),
                    Li("Nam et magna at libero scelerisque egestas."),
                    Li("Suspendisse id nisl ut leo finibus vehicula quis eu ex."),
                    Li("Proin ultricies turpis et volutpat vehicula.")
                ),
                
                # Inline text elements
                H3("Inline text elements"),
                Div(
                    P(A("Primary link", href="#", onclick="event.preventDefault()")),
                    P(A("Secondary link", href="#", class_="secondary", onclick="event.preventDefault()")),
                    P(A("Contrast link", href="#", class_="contrast", onclick="event.preventDefault()")),
                    class_="grid"
                ),
                Div(
                    P(Strong("Bold")),
                    P(Em("Italic")),
                    P(U("Underline")),
                    class_="grid"
                ),
                Div(
                    P(Del("Deleted")),
                    P(Ins("Inserted")),
                    P(S("Strikethrough")),
                    class_="grid"
                ),
                Div(
                    P(Small("Small ")),
                    P("Text ", Sub("Sub")),
                    P("Text ", Sup("Sup")),
                    class_="grid"
                ),
                Div(
                    P(Abbr("Abbr.", title="Abbreviation", **{"data-tooltip": "Abbreviation"})),
                    P(Kbd("Kbd")),
                    P(Mark("Highlighted")),
                    class_="grid"
                ),
                
                # Headings
                H3("Heading 3"),
                P("Integer bibendum malesuada libero vel eleifend. Fusce iaculis turpis ipsum, at efficitur sem scelerisque vel. Aliquam auctor diam ut purus cursus fringilla. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos."),
                H4("Heading 4"),
                P("Cras fermentum velit vitae auctor aliquet. Nunc non congue urna, at blandit nibh. Donec ac fermentum felis. Vivamus tincidunt arcu ut lacus hendrerit, eget mattis dui finibus."),
                H5("Heading 5"),
                P("Donec nec egestas nulla. Sed varius placerat felis eu suscipit. Mauris maximus ante in consequat luctus. Morbi euismod sagittis efficitur. Aenean non eros orci. Vivamus ut diam sem."),
                H6("Heading 6"),
                P("Ut sed quam non mauris placerat consequat vitae id risus. Vestibulum tincidunt nulla ut tortor posuere, vitae malesuada tortor molestie. Sed nec interdum dolor. Vestibulum id auctor nisi, a efficitur sem. Aliquam sollicitudin efficitur turpis, sollicitudin hendrerit ligula semper id. Nunc risus felis, egestas eu tristique eget, convallis in velit."),
                
                # Media
                Figure(
                    Img(src="/static/example/img/aleksandar-jason-a562ZEFKW8I-unsplash-2000x1000.jpg", alt="Minimal landscape"),
                    Figcaption(
                        "Image from ",
                        A("unsplash.com", href="https://unsplash.com/photos/a562ZEFKW8I", target="_blank")
                    )
                ),
                id="typography"
            ),
            
            # Buttons section
            Section(
                H2("Buttons"),
                P(
                    Button("Primary"),
                    Button("Secondary", class_="secondary"),
                    Button("Contrast", class_="contrast"),
                    class_="grid"
                ),
                P(
                    Button("Primary outline", class_="outline"),
                    Button("Secondary outline", class_="outline secondary"),
                    Button("Contrast outline", class_="outline contrast"),
                    class_="grid"
                ),
                id="buttons"
            ),
            
            # Form elements section
            Section(
                Form(
                    H2("Form elements"),
                    
                    # Search
                    Label("Search", fr="search"),
                    Input(type="search", id="search", name="search", placeholder="Search"),
                    
                    # Text
                    Label("Text", fr="text"),
                    Input(type="text", id="text", name="text", placeholder="Text"),
                    Small("Curabitur consequat lacus at lacus porta finibus."),
                    
                    # Select
                    Label("Select", fr="select"),
                    Select(
                        Option("Select…", value="", selected=True),
                        Option("…"),
                        id="select", name="select", required=True
                    ),
                    
                    # File browser
                    Label(
                        "File browser",
                        Input(type="file", id="file", name="file")
                    ),
                    
                    # Range slider
                    Label(
                        "Range slider",
                        Input(type="range", min="0", max="100", value="50", id="range", name="range")
                    ),
                    
                    # States
                    Div(
                        Label(
                            "Valid",
                            Input(type="text", id="valid", name="valid", placeholder="Valid", **{"aria-invalid": "false"})
                        ),
                        Label(
                            "Invalid",
                            Input(type="text", id="invalid", name="invalid", placeholder="Invalid", **{"aria-invalid": "true"})
                        ),
                        Label(
                            "Disabled",
                            Input(type="text", id="disabled", name="disabled", placeholder="Disabled", disabled=True)
                        ),
                        class_="grid"
                    ),
                    
                    # Date, Time, Color
                    Div(
                        Label(
                            "Date",
                            Input(type="date", id="date", name="date")
                        ),
                        Label(
                            "Time",
                            Input(type="time", id="time", name="time")
                        ),
                        Label(
                            "Color",
                            Input(type="color", id="color", name="color", value="#0eaaaa")
                        ),
                        class_="grid"
                    ),
                    
                    # Checkboxes, Radio buttons, Switches
                    Div(
                        Fieldset(
                            Legend(Strong("Checkboxes")),
                            Label(
                                Input(type="checkbox", id="checkbox-1", name="checkbox-1", checked=True),
                                " Checkbox"
                            ),
                            Label(
                                Input(type="checkbox", id="checkbox-2", name="checkbox-2"),
                                " Checkbox"
                            )
                        ),
                        
                        Fieldset(
                            Legend(Strong("Radio buttons")),
                            Label(
                                Input(type="radio", id="radio-1", name="radio", value="radio-1", checked=True),
                                " Radio button"
                            ),
                            Label(
                                Input(type="radio", id="radio-2", name="radio", value="radio-2"),
                                " Radio button"
                            )
                        ),
                        
                        Fieldset(
                            Legend(Strong("Switches")),
                            Label(
                                Input(type="checkbox", id="switch-1", name="switch-1", role="switch", checked=True),
                                " Switch"
                            ),
                            Label(
                                Input(type="checkbox", id="switch-2", name="switch-2", role="switch"),
                                " Switch"
                            )
                        ),
                        class_="grid"
                    ),
                    
                    # Form buttons
                    Input(type="reset", value="Reset", onclick="event.preventDefault()"),
                    Input(type="submit", value="Submit", onclick="event.preventDefault()")
                ),
                id="form"
            ),
            
            # Tables section
            Section(
                H2("Tables"),
                Div(
                    Table(
                        Thead(
                            Tr(
                                Th("#", scope="col"),
                                Th("Heading", scope="col"),
                                Th("Heading", scope="col"),
                                Th("Heading", scope="col"),
                                Th("Heading", scope="col"),
                                Th("Heading", scope="col"),
                                Th("Heading", scope="col"),
                                Th("Heading", scope="col")
                            )
                        ),
                        Tbody(
                            Tr(
                                Th("1", scope="row"),
                                Td("Cell"),
                                Td("Cell"),
                                Td("Cell"),
                                Td("Cell"),
                                Td("Cell"),
                                Td("Cell"),
                                Td("Cell")
                            ),
                            Tr(
                                Th("2", scope="row"),
                                Td("Cell"),
                                Td("Cell"),
                                Td("Cell"),
                                Td("Cell"),
                                Td("Cell"),
                                Td("Cell"),
                                Td("Cell")
                            ),
                            Tr(
                                Th("3", scope="row"),
                                Td("Cell"),
                                Td("Cell"),
                                Td("Cell"),
                                Td("Cell"),
                                Td("Cell"),
                                Td("Cell"),
                                Td("Cell")
                            )
                        ),
                        class_="striped"
                    ),
                    class_="overflow-auto"
                ),
                id="tables"
            ),
            
            # Modal section
            Section(
                H2("Modal"),
                Button("Launch demo modal", class_="contrast", **{"data-target": "modal-example", "onclick": "toggleModal(event)"}),
                id="modal"
            ),
            
            # Accordions section
            Section(
                H2("Accordions"),
                Details(
                    Summary("Accordion 1"),
                    P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque urna diam, tincidunt nec porta sed, auctor id velit. Etiam venenatis nisl ut orci consequat, vitae tempus quam commodo. Nulla non mauris ipsum. Aliquam eu posuere orci. Nulla convallis lectus rutrum quam hendrerit, in facilisis elit sollicitudin. Mauris pulvinar pulvinar mi, dictum tristique elit auctor quis. Maecenas ac ipsum ultrices, porta turpis sit amet, congue turpis.")
                ),
                Details(
                    Summary("Accordion 2"),
                    Ul(
                        Li("Vestibulum id elit quis massa interdum sodales."),
                        Li("Nunc quis eros vel odio pretium tincidunt nec quis neque."),
                        Li("Quisque sed eros non eros ornare elementum."),
                        Li("Cras sed libero aliquet, porta dolor quis, dapibus ipsum.")
                    ),
                    open=True
                ),
                id="accordions"
            ),
            
            # Article section
            Article(
                H2("Article"),
                P("Nullam dui arcu, malesuada et sodales eu, efficitur vitae dolor. Sed ultricies dolor non ante vulputate hendrerit. Vivamus sit amet suscipit sapien. Nulla iaculis eros a elit pharetra egestas. Nunc placerat facilisis cursus. Sed vestibulum metus eget dolor pharetra rutrum."),
                Footer(
                    Small("Duis nec elit placerat, suscipit nibh quis, finibus neque.")
                ),
                id="article"
            ),
            
            # Group section
            Section(
                H2("Group"),
                Form(
                    Fieldset(
                        Input(name="email", type="email", placeholder="Enter your email", autocomplete="email"),
                        Input(type="submit", value="Subscribe"),
                        role="group"
                    )
                ),
                id="group"
            ),
            
            # Progress section
            Section(
                H2("Progress bar"),
                Progress(id="progress-1", value="25", max="100"),
                Progress(id="progress-2"),
                id="progress"
            ),
            
            # Loading section
            Section(
                H2("Loading"),
                Article(**{"aria-busy": "true"}),
                Button("Please wait…", **{"aria-busy": "true"}),
                id="loading"
            ),
            
            class_="container"
        ),
        
        # Footer
        Footer(
            Small(
                "Built with ",
                A("Pico", href="https://picocss.com"),
                " • ",
                A("Source code", href="https://github.com/picocss/examples/blob/master/v2-html/index.html")
            ),
            class_="container"
        ),
        
        # Modal example
        Dialog(
            Article(
                Header(
                    Button(**{"aria-label": "Close", "rel": "prev", "data-target": "modal-example", "onclick": "toggleModal(event)"}),
                    H3("Confirm your action!")
                ),
                P("Cras sit amet maximus risus. Pellentesque sodales odio sit amet augue finibus pellentesque. Nullam finibus risus non semper euismod."),
                Footer(
                    Button("Cancel", role="button", class_="secondary", **{"data-target": "modal-example", "onclick": "toggleModal(event)"}),
                    Button("Confirm", autofocus=True, **{"data-target": "modal-example", "onclick": "toggleModal(event)"})
                )
            ),
            id="modal-example"
        )
    )

@rt('/static/example/<path:path>')
def get_static(path):
    return send_from_directory('example', path)

# Add CSS styling with custom headers
app.hdrs += (
    # Google Fonts - Source Sans 3
    Link(rel="preconnect", href="https://fonts.googleapis.com"),
    Link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin=True),
    Link(href="https://fonts.googleapis.com/css2?family=Source+Sans+3:ital,wght@0,200..900;1,200..900&display=swap", rel="stylesheet"),
    
    # Custom Pico CSS
    Link(rel="stylesheet", href="/static/pico.css"),
    
    # Apply Source Sans 3 font
    Style(font_style),
    
    # Theme switcher script
    Script(theme_switcher_js),
    
    # Modal script
    Script(modal_js)
)

# Get port from environment variable if set
port = int(os.environ.get('FASTHTML_PORT', 5004))

# Start the server
if __name__ == "__main__":
    print(f"Starting FastHTML server. Visit http://localhost:{port} to see the Pico CSS example.")
    print(f"Make sure you have the image in example/img/ folder!")
    serve(port=port) 