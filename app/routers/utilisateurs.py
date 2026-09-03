from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..security import get_current_user

router = APIRouter(prefix="/utilisateurs", tags=["Utilisateurs"])


@router.get("", response_model=list[schemas.UtilisateurResponse])
def lister_utilisateurs(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _utilisateur=Depends(get_current_user),
):
    return crud.get_utilisateurs(db, skip=skip, limit=limit)


@router.get("/{utilisateur_id}", response_model=schemas.UtilisateurResponse)
def obtenir_utilisateur(
    utilisateur_id: int,
    db: Session = Depends(get_db),
    _utilisateur=Depends(get_current_user),
):
    utilisateur = crud.get_utilisateur(db, utilisateur_id)
    if utilisateur is None:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return utilisateur


@router.post("", response_model=schemas.UtilisateurResponse, status_code=201)
def creer_utilisateur(
    utilisateur: schemas.UtilisateurCreate,
    db: Session = Depends(get_db),
    _utilisateur=Depends(get_current_user),
):
    return crud.create_utilisateur(db, utilisateur)


@router.put("/{utilisateur_id}", response_model=schemas.UtilisateurResponse)
def modifier_utilisateur(
    utilisateur_id: int,
    utilisateur: schemas.UtilisateurCreate,
    db: Session = Depends(get_db),
    _utilisateur=Depends(get_current_user),
):
    utilisateur_existant = crud.get_utilisateur(db, utilisateur_id)
    if utilisateur_existant is None:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return crud.update_utilisateur(db, utilisateur_existant, utilisateur)


@router.delete("/{utilisateur_id}", status_code=204)
def supprimer_utilisateur(
    utilisateur_id: int,
    db: Session = Depends(get_db),
    _utilisateur=Depends(get_current_user),
):
    utilisateur = crud.get_utilisateur(db, utilisateur_id)
    if utilisateur is None:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    crud.delete(db, utilisateur)