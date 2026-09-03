from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])


@router.get("", response_model=list[schemas.UtilisateurResponse])
def lister_utilisateurs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return crud.get_utilisateurs(db, skip=skip, limit=limit)


@router.get("/{utilisateur_id}", response_model=schemas.UtilisateurResponse)
def obtenir_utilisateur(utilisateur_id: int, db: Session = Depends(get_db)):
    utilisateur = crud.get_utilisateur(db, utilisateur_id)
    if utilisateur is None:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return utilisateur


@router.post("", response_model=schemas.UtilisateurResponse, status_code=201)
def creer_utilisateur(
    utilisateur: schemas.UtilisateurCreate,
    db: Session = Depends(get_db),
):
    return crud.create_utilisateur(db, utilisateur)