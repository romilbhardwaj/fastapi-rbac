import casbin
import os
from fastapi import HTTPException

# Initialize Casbin enforcer
def get_enforcer():
    """Initialize Casbin enforcer with model and policy"""
    # Get the directory where this file is located
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    model_path = os.path.join(current_dir, "casbin", "model.conf")
    policy_path = os.path.join(current_dir, "casbin", "policy.csv")
    
    enforcer = casbin.Enforcer(model_path, policy_path)
    return enforcer

def check_permission(username: str, action: str, resource: str):
    """Check if user has permission to perform action on resource"""
    enforcer = get_enforcer()
    
    # Check permission
    allowed = enforcer.enforce(username, resource, action)
    
    if not allowed:
        raise HTTPException(
            status_code=403, 
            detail=f"Access denied: User '{username}' cannot '{action}' on '{resource}'"
        )
    
    return True 