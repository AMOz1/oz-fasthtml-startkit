from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import sqlite3
import os
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-here")  # Change in production
templates = Jinja2Templates(directory="templates")

ADMIN_PASSWORD = "nulaR0rula"  # Your specified password

def get_db_connection():
    """Connect to SQLite database"""
    conn = sqlite3.connect('radio.db')
    conn.row_factory = sqlite3.Row
    return conn

def search_tracks(query):
    """Search tracks in the database"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    words = query.split()
    if not words:
        return []
    
    # Search for tracks containing all words (case-insensitive)
    sql_conditions = " AND ".join(["LOWER(track) LIKE ?" for _ in words])
    sql_query = f"SELECT DISTINCT track FROM tracks WHERE {sql_conditions} ORDER BY track"
    params = [f"%{word.lower()}%" for word in words]
    
    cursor.execute(sql_query, params)
    results = cursor.fetchall()
    conn.close()
    
    return [dict(row) for row in results]

# Create templates directory
if not os.path.exists("templates"):
    os.makedirs("templates")

# Create the login template
with open("templates/login.html", "w") as f:
    f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Radio NULA - Login</title>
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <style>
        @import "tailwindcss";
        @plugin "daisyui" {
            themes: light --default;
        }
    </style>
</head>
<body class="min-h-screen bg-base-200 flex items-center justify-center">
    <div class="card bg-base-100 shadow-xl w-96">
        <div class="card-body">
            <h1 class="card-title text-2xl mb-6 justify-center">Radio NULA</h1>
            <form method="POST" action="/login" class="space-y-4">
                {% if error %}
                <div class="alert alert-error">
                    <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                    <span>{{ error }}</span>
                </div>
                {% endif %}
                <div class="form-control">
                    <input 
                        type="password" 
                        name="password" 
                        placeholder="Enter password" 
                        class="input input-bordered w-full"
                        autofocus
                    >
                </div>
                <button type="submit" class="btn btn-primary w-full">GO</button>
            </form>
        </div>
    </div>
</body>
</html>
    """.strip())

# Create the main template
with open("templates/index.html", "w") as f:
    f.write("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Radio NULA Track Search</title>
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <style>
        @import "tailwindcss";
        @plugin "daisyui" {
            themes: light --default;
        }
    </style>
</head>
<body class="min-h-screen bg-base-200 py-8">
    <div class="container mx-auto px-4 max-w-3xl">
        <div class="card bg-base-100">
            <div class="card-body">
                <div class="flex justify-between items-center mb-8">
                    <h1 class="text-3xl font-bold">Radio NULA track search</h1>
                    <form action="/logout" method="POST">
                        <button type="submit" class="btn btn-ghost btn-sm">Logout</button>
                    </form>
                </div>
                <div class="form-control">
                    <div class="join w-full">
                        <input 
                            id="search-input" 
                            name="q" 
                            type="text" 
                            placeholder="Enter track name or artist..." 
                            class="input input-bordered join-item w-full"
                            hx-post="/search"
                            hx-trigger="keyup changed delay:500ms, search"
                            hx-target="#results"
                            autofocus
                        >
                        <button 
                            type="button" 
                            class="btn btn-primary join-item"
                            hx-post="/search"
                            hx-include="#search-input"
                            hx-target="#results"
                        >Search</button>
                    </div>
                </div>
                <div id="results" class="mt-8">
                    <div class="alert alert-info">
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                        <span>Enter a search term to find tracks</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    """.strip())

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    if not request.session.get("authenticated"):
        return RedirectResponse(url="/login")
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login(request: Request):
    form = await request.form()
    password = form.get("password")
    
    if password == ADMIN_PASSWORD:
        request.session["authenticated"] = True
        return RedirectResponse(url="/", status_code=303)
    
    return templates.TemplateResponse(
        "login.html", 
        {"request": request, "error": "Incorrect password"}
    )

@app.post("/logout")
async def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=303)

@app.post("/search", response_class=HTMLResponse)
async def search(request: Request):
    if not request.session.get("authenticated"):
        return RedirectResponse(url="/login")
        
    form = await request.form()
    q = form.get("q", "").strip()
    
    if not q:
        return HTMLResponse("""
            <div class="alert alert-info">
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                <span>Enter a search term to find tracks</span>
            </div>
        """)
    
    results = search_tracks(q)
    
    if not results:
        return HTMLResponse(f"""
            <div class="alert alert-warning">
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" /></svg>
                <span>No matching tracks found for: {q}</span>
            </div>
        """)
    
    results_html = f"""
        <div>
            <div class="alert alert-success mb-4">
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>Found {len(results)} tracks matching: {q}</span>
            </div>
            <div class="overflow-x-auto">
                <table class="table table-zebra w-full">
                    <thead>
                        <tr>
                            <th>Track</th>
                        </tr>
                    </thead>
                    <tbody>
                        {"".join(f'<tr><td>{result["track"]}</td></tr>' for result in results)}
                    </tbody>
                </table>
            </div>
        </div>
    """
    return HTMLResponse(results_html)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)