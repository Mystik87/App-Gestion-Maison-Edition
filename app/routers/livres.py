from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db
from ..security import get_current_user

router = APIRouter(prefix="/livres", tags=["Livres"])


@router.get("", response_model=list[schemas.LivreResponse])
def lister_livres(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    _utilisateur=Depends(get_current_user),
):
    return crud.get_livres(db, skip=skip, limit=limit)


@router.get("/{livre_id}", response_model=schemas.LivreResponse)
def obtenir_livre(
    livre_id: int,
    db: Session = Depends(get_db),
    _utilisateur=Depends(get_current_user),
):
    livre = crud.get_livre(db, livre_id)
    if livre is None:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    return livre


@router.post("", response_model=schemas.LivreResponse, status_code=201)
def creer_livre(
    livre: schemas.LivreCreate,
    db: Session = Depends(get_db),
    _utilisateur=Depends(get_current_user),
):
    return crud.create_livre(db, livre)


@router.put("/{livre_id}", response_model=schemas.LivreResponse)
def modifier_livre(
    livre_id: int,
    livre: schemas.LivreCreate,
    db: Session = Depends(get_db),
    _utilisateur=Depends(get_current_user),
):
    livre_existant = crud.get_livre(db, livre_id)
    if livre_existant is None:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    return crud.update_livre(db, livre_existant, livre)


@router.delete("/{livre_id}", status_code=204)
def supprimer_livre(
    livre_id: int,
    db: Session = Depends(get_db),
    _utilisateur=Depends(get_current_user),
):
    livre = crud.get_livre(db, livre_id)
    if livre is None:
        raise HTTPException(status_code=404, detail="Livre introuvable")
    crud.delete(db, livre)