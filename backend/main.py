"""
Currency Collector - FastAPI Backend

A production-grade currency collection management system with web UI and API.

## Running Locally
1. Install dependencies: pip install -r requirements.txt
2. Copy .env.example to .env and configure your settings
3. Run: uvicorn main:app --reload --host 0.0.0.0 --port 8000
4. Open: http://localhost:8000

## Environment Variables
- APP_PASSWORD: Shared password for web login
- API_TOKEN: Bearer token for programmatic API access (n8n)
- CSV_PATH: Path to the CSV file (default: ./notes.csv)
- SESSION_SECRET: Random string for signing session cookies
- ALLOW_ORIGIN: CORS origin (default: *)

## CSV Schema
Canonical header order:
note_id,country,pick,grade,purchase_price,epq,pmg_cert,denomination,year,serial,purchase_date,est_value,est_updated_at,notes

Required fields: note_id, country, pick, grade, purchase_price
Optional fields: epq, pmg_cert, denomination, year, serial, purchase_date, est_value, est_updated_at, notes

## API Examples

### Web UI Authentication
```bash
# Login
curl -X POST http://localhost:8000/api/login \
  -H "Content-Type: application/json" \
  -d '{"password": "your_password"}' \
  -c cookies.txt

# Get notes (with session cookie)
curl -X GET http://localhost:8000/api/notes \
  -b cookies.txt
```

### Programmatic API (n8n)
```bash
# Get all notes
curl -X GET http://localhost:8000/api/notes \
  -H "Authorization: Bearer your_api_token"

# Update estimate
curl -X PATCH http://localhost:8000/api/notes/123/estimate \
  -H "Authorization: Bearer your_api_token" \
  -H "Content-Type: application/json" \
  -d '{"est_value": 150.00, "est_updated_at": "2024-01-15T10:30:00Z"}'

# Export CSV
curl -X GET http://localhost:8000/api/notes.csv \
  -H "Authorization: Bearer your_api_token"
```

## Deployment Notes
- Render/Railway: Set environment variables in dashboard
- Ensure CSV_PATH is writable and persistent
- Use HTTPS in production (Secure cookie flag)
- Consider database migration for production scale
"""

import os
import csv
import uuid
import tempfile
from datetime import datetime, timezone
from typing import List, Dict, Optional, Any
from collections import defaultdict
import time

from fastapi import FastAPI, HTTPException, Depends, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
APP_PASSWORD = os.getenv("APP_PASSWORD", "admin123")
API_TOKEN = os.getenv("API_TOKEN", "your-secret-api-token")
CSV_PATH = os.getenv("CSV_PATH", "./sample_notes.csv")
SESSION_SECRET = os.getenv("SESSION_SECRET", "your-session-secret-key")
ALLOW_ORIGIN = os.getenv("ALLOW_ORIGIN", "*")

# Canonical CSV headers in order
CANONICAL_HEADERS = [
    "note_id", "country", "pick", "grade", "purchase_price", "epq", 
    "pmg_cert", "denomination", "year", "serial", "purchase_date", 
    "est_value", "est_updated_at", "notes"
]

# Required fields
REQUIRED_FIELDS = ["note_id", "country", "pick", "grade", "purchase_price"]

# Rate limiting storage (in-memory)
rate_limit_storage = defaultdict(list)

# Initialize FastAPI app
app = FastAPI(
    title="Currency Collector API",
    description="A production-grade currency collection management system",
    version="1.0.0"
)

# Add session middleware
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    max_age=86400,  # 24 hours
    same_site="lax",
    https_only=False  # Set to True in production with HTTPS
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if ALLOW_ORIGIN == "*" else [ALLOW_ORIGIN],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()

# Pydantic models
class LoginRequest(BaseModel):
    password: str

class NoteCreate(BaseModel):
    note_id: Optional[str] = None
    country: str
    pick: str
    grade: float
    purchase_price: float
    epq: Optional[str] = ""
    pmg_cert: Optional[str] = ""
    denomination: Optional[str] = ""
    year: Optional[int] = None
    serial: Optional[str] = ""
    purchase_date: Optional[str] = ""
    est_value: Optional[float] = None
    est_updated_at: Optional[str] = None
    notes: Optional[str] = ""

class NoteUpdate(BaseModel):
    country: Optional[str] = None
    pick: Optional[str] = None
    grade: Optional[float] = None
    purchase_price: Optional[float] = None
    epq: Optional[str] = None
    pmg_cert: Optional[str] = None
    denomination: Optional[str] = None
    year: Optional[int] = None
    serial: Optional[str] = None
    purchase_date: Optional[str] = None
    est_value: Optional[float] = None
    est_updated_at: Optional[str] = None
    notes: Optional[str] = None

class EstimateUpdate(BaseModel):
    est_value: float
    est_updated_at: Optional[str] = None

# CSV Operations
def load_rows() -> List[Dict[str, Any]]:
    """Load all rows from CSV file."""
    if not os.path.exists(CSV_PATH):
        return []
    
    rows = []
    with open(CSV_PATH, 'r', newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Fill missing keys with empty strings
            normalized_row = {key: row.get(key, "") for key in CANONICAL_HEADERS}
            # Convert numeric fields
            if normalized_row.get("grade"):
                try:
                    normalized_row["grade"] = float(normalized_row["grade"])
                except ValueError:
                    pass
            if normalized_row.get("purchase_price"):
                try:
                    normalized_row["purchase_price"] = float(normalized_row["purchase_price"])
                except ValueError:
                    pass
            if normalized_row.get("est_value"):
                try:
                    normalized_row["est_value"] = float(normalized_row["est_value"])
                except ValueError:
                    pass
            if normalized_row.get("year"):
                try:
                    normalized_row["year"] = int(normalized_row["year"]) if normalized_row["year"] else ""
                except ValueError:
                    pass
            rows.append(normalized_row)
    return rows

def save_rows(rows: List[Dict[str, Any]]) -> None:
    """Save rows to CSV file atomically."""
    # Write to temporary file first
    temp_path = f"{CSV_PATH}.tmp"
    with open(temp_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CANONICAL_HEADERS)
        writer.writeheader()
        for row in rows:
            # Ensure all fields are present
            normalized_row = {key: row.get(key, "") for key in CANONICAL_HEADERS}
            writer.writerow(normalized_row)
    
    # Atomic rename
    os.replace(temp_path, CSV_PATH)

def upsert_row(row: Dict[str, Any]) -> str:
    """Upsert a row by note_id."""
    rows = load_rows()
    note_id = row.get("note_id") or str(uuid.uuid4())
    row["note_id"] = note_id
    
    # Find existing row
    existing_index = None
    for i, existing_row in enumerate(rows):
        if existing_row["note_id"] == note_id:
            existing_index = i
            break
    
    if existing_index is not None:
        # Update existing row
        rows[existing_index].update(row)
    else:
        # Add new row
        rows.append(row)
    
    save_rows(rows)
    return note_id

def delete_row(note_id: str) -> bool:
    """Delete a row by note_id."""
    rows = load_rows()
    original_count = len(rows)
    rows = [row for row in rows if row["note_id"] != note_id]
    
    if len(rows) < original_count:
        save_rows(rows)
        return True
    return False

def get_row_by_id(note_id: str) -> Optional[Dict[str, Any]]:
    """Get a row by note_id."""
    rows = load_rows()
    for row in rows:
        if row["note_id"] == note_id:
            return row
    return None

# Authentication
def require_session(request: Request):
    """Require valid session for UI operations."""
    if not request.session.get("authenticated"):
        raise HTTPException(status_code=401, detail="Authentication required")
    return True

def require_bearer(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Require valid Bearer token for API operations."""
    if credentials.credentials != API_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid API token")
    return True

# Rate limiting
def check_rate_limit(request: Request, limit: int = 30, window: int = 60):
    """Simple rate limiting per IP."""
    client_ip = request.client.host
    current_time = time.time()
    key = f"{client_ip}:{request.url.path}"
    
    # Clean old entries
    rate_limit_storage[key] = [
        timestamp for timestamp in rate_limit_storage[key]
        if current_time - timestamp < window
    ]
    
    # Check limit
    if len(rate_limit_storage[key]) >= limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    # Add current request
    rate_limit_storage[key].append(current_time)

# API Endpoints

@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"ok": True}

@app.post("/api/login")
async def login(request: Request, login_data: LoginRequest):
    """Login with password to set session cookie."""
    if login_data.password != APP_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid password")
    
    request.session["authenticated"] = True
    return {"message": "Login successful"}

@app.get("/api/logout")
async def logout(request: Request):
    """Logout and clear session."""
    request.session.clear()
    return {"message": "Logout successful"}

@app.get("/api/notes")
async def get_notes(
    request: Request,
    country: Optional[str] = None,
    pick: Optional[str] = None,
    min_grade: Optional[float] = None,
    max_grade: Optional[float] = None,
    search: Optional[str] = None,
    _: bool = Depends(require_session)
):
    """Get all notes with optional filtering."""
    rows = load_rows()
    
    # Apply filters
    if country:
        rows = [row for row in rows if country.lower() in row.get("country", "").lower()]
    if pick:
        rows = [row for row in rows if pick.lower() in row.get("pick", "").lower()]
    if min_grade is not None:
        rows = [row for row in rows if row.get("grade", 0) >= min_grade]
    if max_grade is not None:
        rows = [row for row in rows if row.get("grade", 0) <= max_grade]
    if search:
        search_lower = search.lower()
        rows = [
            row for row in rows
            if any(search_lower in str(value).lower() for value in row.values())
        ]
    
    return rows

@app.get("/api/notes.csv")
async def get_notes_csv(request: Request, _: bool = Depends(require_session)):
    """Export notes as CSV."""
    rows = load_rows()
    
    def generate_csv():
        yield ",".join(CANONICAL_HEADERS) + "\n"
        for row in rows:
            yield ",".join(f'"{str(row.get(key, ""))}"' for key in CANONICAL_HEADERS) + "\n"
    
    return StreamingResponse(
        generate_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=notes.csv"}
    )

@app.post("/api/notes")
async def create_note(
    request: Request,
    note_data: NoteCreate,
    _: bool = Depends(require_session)
):
    """Create a new note."""
    check_rate_limit(request)
    
    # Generate note_id if not provided
    if not note_data.note_id:
        note_data.note_id = str(uuid.uuid4())
    
    # Check if note_id already exists
    if get_row_by_id(note_data.note_id):
        raise HTTPException(status_code=409, detail="Note ID already exists")
    
    note_dict = note_data.dict()
    note_id = upsert_row(note_dict)
    
    return {"message": "Note created successfully", "note_id": note_id}

@app.put("/api/notes/{note_id}")
async def update_note(
    request: Request,
    note_id: str,
    note_data: NoteUpdate,
    _: bool = Depends(require_session)
):
    """Update a note by ID."""
    check_rate_limit(request)
    
    existing_row = get_row_by_id(note_id)
    if not existing_row:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Update only provided fields, excluding None values
    update_data = {k: v for k, v in note_data.dict().items() if v is not None}
    update_data["note_id"] = note_id
    
    # Merge with existing data to preserve unchanged fields
    merged_data = existing_row.copy()
    merged_data.update(update_data)
    
    upsert_row(merged_data)
    return {"message": "Note updated successfully"}

@app.delete("/api/notes/{note_id}")
async def delete_note(
    request: Request,
    note_id: str,
    _: bool = Depends(require_session)
):
    """Delete a note by ID."""
    check_rate_limit(request)
    
    if not delete_row(note_id):
        raise HTTPException(status_code=404, detail="Note not found")
    
    return {"message": "Note deleted successfully"}

@app.post("/api/import")
async def import_csv(
    request: Request,
    file: UploadFile = File(...),
    _: bool = Depends(require_session)
):
    """Import CSV file and upsert notes."""
    check_rate_limit(request)
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV")
    
    content = await file.read()
    csv_content = content.decode('utf-8')
    
    # Parse CSV
    rows = []
    csv_reader = csv.DictReader(csv_content.splitlines())
    for row in csv_reader:
        # Normalize row to canonical headers
        normalized_row = {key: row.get(key, "") for key in CANONICAL_HEADERS}
        rows.append(normalized_row)
    
    # Upsert each row
    imported_count = 0
    for row in rows:
        if row.get("note_id"):
            upsert_row(row)
            imported_count += 1
    
    return {"message": f"Imported {imported_count} notes successfully"}

@app.patch("/api/notes/{note_id}/estimate")
async def update_estimate(
    note_id: str,
    estimate_data: EstimateUpdate,
    _: bool = Depends(require_bearer)
):
    """Update estimate value for a note (n8n integration)."""
    existing_row = get_row_by_id(note_id)
    if not existing_row:
        raise HTTPException(status_code=404, detail="Note not found")
    
    # Set est_updated_at if not provided
    est_updated_at = estimate_data.est_updated_at
    if not est_updated_at:
        est_updated_at = datetime.now(timezone.utc).isoformat()
    
    update_data = {
        "note_id": note_id,
        "est_value": estimate_data.est_value,
        "est_updated_at": est_updated_at
    }
    
    upsert_row(update_data)
    return {"message": "Estimate updated successfully"}

# Serve static files
@app.get("/")
async def serve_index():
    """Serve the main HTML file."""
    import os
    static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "index.html")
    return FileResponse(static_path)

@app.get("/static/{filename}")
async def serve_static(filename: str):
    """Serve static files."""
    import os
    static_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", filename)
    return FileResponse(static_path)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
