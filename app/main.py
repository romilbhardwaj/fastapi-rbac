from fastapi import FastAPI, Depends, HTTPException, status, Form
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth import verify_token, create_access_token
from app.rbac import check_permission

app = FastAPI(
    title="Simple FastAPI RBAC Demo",
    description="Two endpoints with different role access",
    version="1.0.0",
)

security = HTTPBearer()

# Simple in-memory users for demo
DEMO_USERS = {
    "admin": {"username": "admin", "role": "admin", "password": "admin123"},
    "user": {"username": "user", "role": "user", "password": "user123"},
    "viewer": {"username": "viewer", "role": "viewer", "password": "view123"}
}

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Extract user from JWT token"""
    token = credentials.credentials
    username = verify_token(token)
    if username not in DEMO_USERS:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return DEMO_USERS[username]

@app.get("/")
async def root():
    return {
        "message": "Simple FastAPI RBAC Demo",
        "demo_users": {
            "admin": "admin123",
            "user": "user123", 
            "viewer": "view123"
        },
        "endpoints": {
            "/login": "POST - Get JWT token",
            "/admin-only": "GET - Admin access only",
            "/user-content": "GET - User and Admin access"
        }
    }

@app.post("/login")
async def login(username: str = Form(), password: str = Form()):
    """Simple login to get JWT token"""
    if username not in DEMO_USERS or DEMO_USERS[username]["password"] != password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token(username)
    return {"access_token": token, "token_type": "bearer"}

@app.get("/admin-only")
async def admin_endpoint(current_user: dict = Depends(get_current_user)):
    """Endpoint only accessible by admin role"""
    check_permission(current_user["username"], "read", "admin_resource")
    return {
        "message": "🔒 This is ADMIN-ONLY content!",
        "user": current_user["username"],
        "role": current_user["role"],
        "data": "Super secret admin data here..."
    }

@app.get("/user-content")
async def user_endpoint(current_user: dict = Depends(get_current_user)):
    """Endpoint accessible by user and admin roles"""
    check_permission(current_user["username"], "read", "user_resource")
    return {
        "message": "👥 This content is for users and admins",
        "user": current_user["username"],
        "role": current_user["role"],
        "data": "Regular user content here..."
    } 