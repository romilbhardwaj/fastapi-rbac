# Simple FastAPI RBAC Demo

A minimal demonstration of Role-Based Access Control (RBAC) using FastAPI and Casbin.

## Features

- **2 Protected Endpoints** with different role requirements
- **3 Demo Users** with different roles (admin, user, viewer)
- **JWT Authentication** for secure access
- **Casbin RBAC** for permission management

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Test the API** at `http://localhost:8000`

## Demo Users

| Username | Password | Role    | Access                  |
|----------|----------|---------|-------------------------|
| admin    | admin123 | admin   | ✅ Both endpoints       |
| user     | user123  | user    | ✅ User content only    |
| viewer   | view123  | viewer  | ❌ No access to either  |

## API Endpoints

### 🔓 Public Endpoints

- `GET /` - Welcome page with demo info
- `POST /login` - Get JWT token

### 🔒 Protected Endpoints

- `GET /admin-only` - **Admin access only**
- `GET /user-content` - **User and Admin access**

## Usage Examples

### 1. Login to get a token:

```bash
curl -X POST "http://localhost:8000/login" \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### 2. Access protected endpoint:

```bash
curl -X GET "http://localhost:8000/admin-only" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### 3. Test different users:

**Admin (can access both endpoints):**
```bash
# Login as admin
curl -X POST "http://localhost:8000/login" \
  -d "username=admin&password=admin123"

# Access admin endpoint ✅
curl -X GET "http://localhost:8000/admin-only" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"

# Access user endpoint ✅  
curl -X GET "http://localhost:8000/user-content" \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN"
```

**User (can only access user content):**
```bash
# Login as user
curl -X POST "http://localhost:8000/login" \
  -d "username=user&password=user123"

# Access admin endpoint ❌ (403 Forbidden)
curl -X GET "http://localhost:8000/admin-only" \
  -H "Authorization: Bearer YOUR_USER_TOKEN"

# Access user endpoint ✅
curl -X GET "http://localhost:8000/user-content" \
  -H "Authorization: Bearer YOUR_USER_TOKEN"
```

**Viewer (no access to protected content):**
```bash
# Login as viewer
curl -X POST "http://localhost:8000/login" \
  -d "username=viewer&password=view123"

# Access any endpoint ❌ (403 Forbidden)
curl -X GET "http://localhost:8000/user-content" \
  -H "Authorization: Bearer YOUR_VIEWER_TOKEN"
```

## RBAC Configuration

The role-based permissions are defined in `app/casbin/policy.csv`:

```csv
# Role assignments
g, admin, admin_role
g, user, user_role
g, viewer, viewer_role

# Permissions  
p, admin_role, admin_resource, read
p, admin_role, user_resource, read
p, user_role, user_resource, read
```

## Project Structure

```
rbac-example/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI app with endpoints
│   ├── auth.py              # JWT authentication
│   ├── rbac.py              # Casbin RBAC logic
│   └── casbin/
│       ├── model.conf       # RBAC model definition
│       └── policy.csv       # Role assignments & permissions
├── requirements.txt
└── README.md
```

## Interactive Testing

Visit `http://localhost:8000/docs` for the interactive Swagger UI where you can:

1. Use the `/login` endpoint to get a token
2. Click "Authorize" and enter `Bearer YOUR_TOKEN`
3. Test the protected endpoints

## Expected Behavior

- **Admin**: Can access both `/admin-only` and `/user-content`
- **User**: Can access `/user-content` but gets 403 on `/admin-only`
- **Viewer**: Gets 403 on both protected endpoints
- **No token**: Gets 401 Unauthorized

This demonstrates a working RBAC system where permissions are enforced at the endpoint level using Casbin! 