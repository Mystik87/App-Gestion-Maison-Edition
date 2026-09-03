from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import schemas
from ..database import get_db
from ..security import authenticate_user, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/login", response_model=schemas.Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    utilisateur = authenticate_user(db, form_data.username, form_data.password)
    if utilisateur is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {
        "access_token": create_access_token(utilisateur.email),
        "token_type": "bearer",
    }


@router.get("/me", response_model=schemas.UtilisateurResponse)
def obtenir_profil(utilisateur=Depends(get_current_user)):
    return utilisateur