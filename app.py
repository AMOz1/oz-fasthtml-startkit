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
            <div style="margin: 0; padding: 0;">Enter a search term to find tracks</div>
        """)
    
    results = search_tracks(q)
    
    if not results:
        # Use a simple div without role="alert"
        return HTMLResponse(f"""
            <div style="margin: 0; padding: 0;">No matching tracks found for: {q}</div>
        """)
    
    # Add inline style to reset margin/padding on the main result wrapper
    results_html = f"""
        <div style="margin: 0; padding: 0;">
            <small>Found {len(results)} tracks matching: {q}</small>
            <table>
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
    """
    return HTMLResponse(results_html)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5001)