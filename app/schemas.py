from pydantic import BaseModel
from typing import Optional


# ============================================================
# SCHÉMAS UTILISATEUR
# ============================================================

class UtilisateurBase(BaseModel):
    nom: str
    prenom: str
    email: str
    role: str


class UtilisateurCreate(UtilisateurBase):
    mot_de_passe: str


class UtilisateurResponse(UtilisateurBase):
    id: int

    class Config:
        from_attributes = True


# ============================================================
# SCHÉMAS AUTEUR
# ============================================================

class AuteurBase(BaseModel):
    nom: str
    prenom: str
    email: Optional[str] = None
    telephone: Optional[str] = None


class AuteurCreate(AuteurBase):
    pass


class AuteurResponse(AuteurBase):
    id: int

    class Config:
        from_attributes = True


# ============================================================
# SCHÉMAS LIVRE
# ============================================================

class LivreBase(BaseModel):
    titre: str
    isbn: Optional[str] = None
    prix: float
    stock: int = 0
    description: Optional[str] = None


class LivreCreate(LivreBase):
    auteur_id: int


class LivreResponse(LivreBase):
    id: int
    auteur_id: int

    class Config:
        from_attributes = True


# ============================================================
# SCHÉMAS CLIENT
# ============================================================

class ClientBase(BaseModel):
    nom: str
    prenom: str
    email: Optional[str] = None
    telephone: Optional[str] = None
    adresse: Optional[str] = None


class ClientCreate(ClientBase):
    pass


class ClientResponse(ClientBase):
    id: int

    class Config:
        from_attributes = True


# ============================================================
# SCHÉMAS VENTE
# ============================================================

class VenteBase(BaseModel):
    quantite: int
    prix_unitaire: float


class VenteCreate(VenteBase):
    livre_id: int
    client_id: int


class VenteResponse(VenteBase):
    id: int
    livre_id: int
    client_id: int
    montant_total: float

    class Config:
        from_attributes = True