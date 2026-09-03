from datetime import datetime
from typing import Any, TypeVar

from pydantic import BaseModel
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import models, schemas

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
password_hash = PasswordHash.recommended()


def get_by_id(
    db: Session,
    model: type[ModelType],
    object_id: int,
) -> ModelType | None:
    return db.get(model, object_id)


def get_many(
    db: Session,
    model: type[ModelType],
    *,
    skip: int = 0,
    limit: int = 100,
) -> list[ModelType]:
    statement = select(model).offset(skip).limit(limit)
    return list(db.scalars(statement).all())


def create(
    db: Session,
    model: type[ModelType],
    data: CreateSchemaType | dict[str, Any],
) -> ModelType:
    values = (
        data.model_dump()
        if hasattr(data, "model_dump")
        else data.dict()
        if hasattr(data, "dict")
        else data
    )
    instance = model(**values)  # type: ignore[call-arg]
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def update(
    db: Session,
    instance: ModelType,
    data: BaseModel | dict[str, Any],
) -> ModelType:
    values = data.model_dump(exclude_unset=True) if isinstance(data, BaseModel) else data
    for field, value in values.items():
        setattr(instance, field, value)

    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def delete(db: Session, instance: ModelType) -> None:
    db.delete(instance)
    db.commit()


def get_utilisateur(db: Session, utilisateur_id: int) -> models.Utilisateur | None:
    return get_by_id(db, models.Utilisateur, utilisateur_id)


def get_utilisateurs(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Utilisateur]:
    return get_many(db, models.Utilisateur, skip=skip, limit=limit)


def create_utilisateur(
    db: Session,
    data: schemas.UtilisateurCreate,
) -> models.Utilisateur:
    values = data.model_dump()
    values["mot_de_passe"] = password_hash.hash(values["mot_de_passe"])
    values["date_creation"] = datetime.now()
    return create(db, models.Utilisateur, values)


def update_utilisateur(
    db: Session,
    utilisateur: models.Utilisateur,
    data: schemas.UtilisateurCreate,
) -> models.Utilisateur:
    values = data.model_dump()
    values["mot_de_passe"] = password_hash.hash(values["mot_de_passe"])
    return update(db, utilisateur, values)


def get_livre(db: Session, livre_id: int) -> models.Livre | None:
    return get_by_id(db, models.Livre, livre_id)


def get_livres(
    db: Session,
    *,
    skip: int = 0,
    limit: int = 100,
) -> list[models.Livre]:
    return get_many(db, models.Livre, skip=skip, limit=limit)


def create_livre(
    db: Session,
    data: schemas.LivreCreate,
) -> models.Livre:
    values = data.model_dump()
    values.pop("stock", None)
    values["date_creation"] = datetime.now()
    values["statut"] = "disponible"
    return create(db, models.Livre, values)


def update_livre(
    db: Session,
    livre: models.Livre,
    data: schemas.LivreCreate,
) -> models.Livre:
    values = data.model_dump()
    values.pop("stock", None)
    return update(db, livre, values)
