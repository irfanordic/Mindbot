from fastapi import Security, HTTPException, status, Depends
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.tenant import Tenant





API_KEY_HEADER  = APIKeyHeader(name="X_API_KEY", auto_error=True)


async def get_current_tenant(
    req_api_key: str=  Security(API_KEY_HEADER),
    db: Session=Depends(get_db)
) -> Tenant:
    """
    Validates the API key and returns the authenticated Tenant object.
    """
    
    
    try:
        tenant = db.query(Tenant).filter(Tenant.api_key == req_api_key).first()
        if not tenant:
            raise HTTPException (
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="api key is invalid"
                
            )
            
        if not tenant.is_active:
            raise HTTPException (
                status_code=status.HTTP_403_FORBIDDEN,
                detail="user is not active anymore "
            )  
            
            
        return tenant
    
    except HTTPException:
        raise 
            
    except Exception as  e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"cant proceed because of :{str(e)}"
        )
            
    
    