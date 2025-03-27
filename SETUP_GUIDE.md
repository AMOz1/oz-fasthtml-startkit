# Setting Up a Python Web Application with DaisyUI and Tailwind

This guide explains how to set up a modern Python web application using FastAPI, HTMX, DaisyUI 5, and Tailwind CSS 4.

## Project Structure

A typical project structure looks like this:
```
your-project/
├── venv/                  # Python virtual environment
├── app.py                 # Main FastAPI application
├── templates/             # HTML templates
├── static/               # Static files (if needed)
├── requirements.txt      # Python dependencies
└── README.md            # Project documentation
```

## Step 1: Python Environment Setup

1. Create a new project directory:
   ```bash
   mkdir your-project
   cd your-project
   ```

2. Create and activate a virtual environment:
   ```bash
   # Create virtual environment
   python3 -m venv venv

   # Activate on macOS/Linux
   source venv/bin/activate

   # Activate on Windows
   .\venv\Scripts\activate
   ```

3. Install Python dependencies:
   ```bash
   pip install fastapi uvicorn jinja2 python-multipart
   pip freeze > requirements.txt
   ```

## Step 2: Frontend Setup (DaisyUI 5 + Tailwind CSS 4)

In your HTML template, include the following in the `<head>` section:

```html
<head>
    <!-- DaisyUI 5 and Tailwind CSS 4 -->
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    
    <!-- Configure DaisyUI -->
    <style>
        @import "tailwindcss";
        @plugin "daisyui" {
            themes: light --default;
        }
    </style>
</head>
```

### Important Notes:
- DaisyUI 5 requires Tailwind CSS 4
- No `tailwind.config.js` is needed (deprecated in Tailwind CSS 4)
- Load DaisyUI after Tailwind CSS
- Use semantic color names (e.g., `primary`, `secondary`) for theme compatibility

## Step 3: Using DaisyUI Components

### Basic Components

1. Buttons:
   ```html
   <!-- Primary button -->
   <button class="btn btn-primary">Click me</button>

   <!-- Other button variants -->
   <button class="btn btn-secondary">Secondary</button>
   <button class="btn btn-accent">Accent</button>
   <button class="btn btn-ghost">Ghost</button>
   ```

2. Input fields:
   ```html
   <!-- Basic input -->
   <input type="text" class="input input-bordered" />

   <!-- With join (input group) -->
   <div class="join">
     <input type="text" class="input input-bordered join-item" />
     <button class="btn btn-primary join-item">Search</button>
   </div>
   ```

3. Cards:
   ```html
   <div class="card bg-base-100">
     <div class="card-body">
       <h2 class="card-title">Title</h2>
       <p>Content goes here</p>
     </div>
   </div>
   ```

4. Alerts:
   ```html
   <div class="alert alert-info">
     <span>Information message</span>
   </div>
   <div class="alert alert-success">
     <span>Success message</span>
   </div>
   <div class="alert alert-warning">
     <span>Warning message</span>
   </div>
   ```

### Layout Best Practices

1. Container and spacing:
   ```html
   <div class="container mx-auto px-4">
     <div class="space-y-4">
       <!-- Content -->
     </div>
   </div>
   ```

2. Responsive design:
   ```html
   <div class="max-w-3xl mx-auto">  <!-- Limit width on larger screens -->
     <div class="grid grid-cols-1 md:grid-cols-2 gap-4">  <!-- Responsive grid -->
       <!-- Content -->
     </div>
   </div>
   ```

## Step 4: Python FastAPI Setup

1. Basic FastAPI application structure:
   ```python
   from fastapi import FastAPI, Request
   from fastapi.responses import HTMLResponse
   from fastapi.templating import Jinja2Templates

   app = FastAPI()
   templates = Jinja2Templates(directory="templates")

   @app.get("/", response_class=HTMLResponse)
   async def home(request: Request):
       return templates.TemplateResponse("index.html", {"request": request})
   ```

2. Run the application:
   ```bash
   uvicorn app:app --reload --port 5001
   ```

## Common Issues and Solutions

1. Styling not working:
   - Ensure DaisyUI is loaded after Tailwind CSS
   - Check browser console for any loading errors
   - Clear browser cache if needed

2. Components not styled:
   - Verify class names match DaisyUI 5 documentation
   - Use semantic color names (e.g., `primary` instead of specific colors)
   - Check component nesting follows DaisyUI guidelines

3. Theme issues:
   - Set a default theme in DaisyUI configuration
   - Use semantic color classes for better theme support
   - Avoid hardcoding colors

## Development Tips

1. Use HTMX for dynamic updates:
   ```html
   <div hx-post="/search" hx-trigger="keyup changed delay:500ms">
     <!-- Dynamic content -->
   </div>
   ```

2. Leverage DaisyUI's semantic colors:
   - Use `base-100` for main background
   - Use `primary` for main actions
   - Use `secondary` for alternative actions
   - Use semantic alert classes (`alert-info`, `alert-success`, etc.)

3. Keep templates clean:
   - Use components consistently
   - Follow DaisyUI's component structure
   - Use utility classes for minor adjustments

## Resources

- [DaisyUI Documentation](https://daisyui.com/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [HTMX Documentation](https://htmx.org/docs) 