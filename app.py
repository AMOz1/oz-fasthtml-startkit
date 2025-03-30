from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import sqlite3
import os
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="your-secret-key-here")  # Change in production
templates = Jinja2Templates(directory="templates")

# Mount the static files directory
app.mount("/static", StaticFiles(directory="css"), name="static")

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

# Ensure templates directory exists
if not os.path.exists("templates"):
    os.makedirs("templates")

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

@app.get("/logout")
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
        # Use a simple div without role="alert"
        return HTMLResponse("""
            <div class="text-gray-500">Enter a search term to find tracks</div>
        """)
    
    results = search_tracks(q)
    
    if not results:
        # Use a simple div without role="alert"
        return HTMLResponse(f"""
            <div class="text-amber-600 dark:text-amber-400 py-2">No matching tracks found for: {q}</div>
        """)
    
    # Add Tailwind classes for better styling
    results_html = f"""
        <div>
            <div class="text-gray-500 text-sm mb-2">Found {len(results)} tracks matching: {q}</div>
            <table class="w-full">
                <thead class="bg-gray-100 dark:bg-gray-800">
                    <tr>
                        <th class="text-left py-2 px-3">Track</th>
                    </tr>
                </thead>
                <tbody>
                    {"".join(f'<tr class="border-b border-gray-200 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-800"><td class="py-3 px-3">{result["track"]}</td></tr>' for result in results)}
                </tbody>
            </table>
        </div>
    """
    return HTMLResponse(results_html)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)