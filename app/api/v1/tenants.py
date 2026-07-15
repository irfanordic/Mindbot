import secrets 
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import  get_db
from app.schemas.tenants import TenantCreate, TenantResponse
from app.models.tenant import Tenant

router = APIRouter()

@router.post("/", response_model=TenantResponse, status_code=status.HTTP_200_OK)
def register_tenant(tenant_in: TenantCreate,db: Session = Depends(get_db) ):
    existing_tenant = db.query(Tenant).filter(Tenant.email == tenant_in.email).first()
    if existing_tenant:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A company with this email is already registered."
        )
        
    generated_key = f"mb_{secrets.token_urlsafe(32)}"
    
    new_tenant = Tenant(
        name=tenant_in.name,
        email=tenant_in.email,
        api_key=generated_key,
        is_active=True
    )
    
    db.add(new_tenant)
    db.commit()
    db.refresh(new_tenant)
    
    
    return new_tenant
    
