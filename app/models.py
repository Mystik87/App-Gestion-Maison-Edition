from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


# ============================================================
# UTILISATEUR
# ============================================================

class Utilisateur(Base):
    __tablename__ = "utilisateur"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    nom: Mapped[str] = mapped_column(String(100), nullable=False)
    prenom: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    mot_de_passe: Mapped[str] = mapped_column(String(255), nullable=False)
    telephone: Mapped[str | None] = mapped_column(String(25), nullable=True)
    role: Mapped[str] = mapped_column(String(30), nullable=False)
    date_creation: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    auteur: Mapped["Auteur | None"] = relationship(
        "Auteur",
        back_populates="utilisateur",
        uselist=False
    )

    editeur: Mapped["Editeur | None"] = relationship(
        "Editeur",
        back_populates="utilisateur",
        uselist=False
    )

    paiements: Mapped[list["Paiement"]] = relationship(
        "Paiement",
        back_populates="utilisateur"
    )

    notifications: Mapped[list["Notification"]] = relationship(
        "Notification",
        back_populates="utilisateur"
    )


# ============================================================
# AUTEUR
# ============================================================

class Auteur(Base):
    __tablename__ = "auteur"

    utilisateur_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("utilisateur.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )

    biographie: Mapped[str | None] = mapped_column(Text, nullable=True)
    date_de_naissance: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    utilisateur: Mapped["Utilisateur"] = relationship(
        "Utilisateur",
        back_populates="auteur"
    )

    manuscrits: Mapped[list["Manuscrit"]] = relationship(
        "Manuscrit",
        back_populates="auteur"
    )

    livres: Mapped[list["Livre"]] = relationship(
        "Livre",
        back_populates="auteur"
    )


# ============================================================
# EDITEUR
# ============================================================

class Editeur(Base):
    __tablename__ = "editeur"

    utilisateur_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("utilisateur.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )

    specialite: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    identifiant: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    utilisateur: Mapped["Utilisateur"] = relationship(
        "Utilisateur",
        back_populates="editeur"
    )

    commentaires: Mapped[list["Commentaire"]] = relationship(
        "Commentaire",
        back_populates="editeur"
    )

    editions: Mapped[list["Edition"]] = relationship(
        "Edition",
        back_populates="editeur"
    )


# ============================================================
# MANUSCRIT
# ============================================================

class Manuscrit(Base):
    __tablename__ = "manuscrit"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    titre: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    fichier: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    date_soumission: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    date_modification: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    statut: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    commentaire: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    auteur_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("auteur.utilisateur_id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )

    auteur: Mapped["Auteur"] = relationship(
        "Auteur",
        back_populates="manuscrits"
    )

    versions: Mapped[list["Version"]] = relationship(
        "Version",
        back_populates="manuscrit"
    )

    commentaires: Mapped[list["Commentaire"]] = relationship(
        "Commentaire",
        back_populates="manuscrit"
    )

    editions: Mapped[list["Edition"]] = relationship(
        "Edition",
        back_populates="manuscrit"
    )


# ============================================================
# VERSION
# ============================================================

class Version(Base):
    __tablename__ = "version"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    numero: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    fichier: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    commentaire: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    date_creation: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    statut: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    auteur_modification: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    manuscrit_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("manuscrit.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )

    manuscrit: Mapped["Manuscrit"] = relationship(
        "Manuscrit",
        back_populates="versions"
    )

    commentaires: Mapped[list["Commentaire"]] = relationship(
        "Commentaire",
        back_populates="version"
    )


# ============================================================
# COMMENTAIRE
# ============================================================

class Commentaire(Base):
    __tablename__ = "commentaire"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    contenu: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    date_creation: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    statut: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    version_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("version.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True
    )

    editeur_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("editeur.utilisateur_id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True
    )

    manuscrit_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("manuscrit.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=True
    )

    version: Mapped["Version | None"] = relationship(
        "Version",
        back_populates="commentaires"
    )

    editeur: Mapped["Editeur | None"] = relationship(
        "Editeur",
        back_populates="commentaires"
    )

    manuscrit: Mapped["Manuscrit | None"] = relationship(
        "Manuscrit",
        back_populates="commentaires"
    )


# ============================================================
# LIVRE
# ============================================================

class Livre(Base):
    __tablename__ = "livre"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    titre: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    isbn: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    genre: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    nombre_page: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    prix: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    date_creation: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    statut: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    auteur_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("auteur.utilisateur_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )

    auteur: Mapped["Auteur"] = relationship(
        "Auteur",
        back_populates="livres"
    )

    editions: Mapped[list["Edition"]] = relationship(
        "Edition",
        back_populates="livre"
    )

    publication: Mapped["Publication | None"] = relationship(
        "Publication",
        back_populates="livre",
        uselist=False
    )


# ============================================================
# EDITION
# ============================================================

class Edition(Base):
    __tablename__ = "edition"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    date_debut: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    date_fin: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    statut: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    nombre_exemplaires: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    format: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    couverture: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    prix: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    manuscrit_id: Mapped[int | None] = mapped_column(
        BigInteger,
        ForeignKey("manuscrit.id", ondelete="SET NULL", onupdate="CASCADE"),
        nullable=True
    )

    editeur_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("editeur.utilisateur_id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )

    livre_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("livre.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )

    manuscrit: Mapped["Manuscrit | None"] = relationship(
        "Manuscrit",
        back_populates="editions"
    )

    editeur: Mapped["Editeur"] = relationship(
        "Editeur",
        back_populates="editions"
    )

    livre: Mapped["Livre"] = relationship(
        "Livre",
        back_populates="editions"
    )


# ============================================================
# PUBLICATION
# ============================================================

class Publication(Base):
    __tablename__ = "publication"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    date_publication: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    statut: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    format: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    lien_publication: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    nombre_exemplaire: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    date_creation: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    livre_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("livre.id", ondelete="CASCADE", onupdate="CASCADE"),
        unique=True,
        nullable=False
    )

    livre: Mapped["Livre"] = relationship(
        "Livre",
        back_populates="publication"
    )


# ============================================================
# PAIEMENT
# ============================================================

class Paiement(Base):
    __tablename__ = "paiement"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    montant: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )

    date_paiement: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    mode_paiement: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    reference: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    statut: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    transaction_id: Mapped[str | None] = mapped_column(
        String(150),
        nullable=True
    )

    utilisateur_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("utilisateur.id", ondelete="RESTRICT", onupdate="CASCADE"),
        nullable=False
    )

    utilisateur: Mapped["Utilisateur"] = relationship(
        "Utilisateur",
        back_populates="paiements"
    )


# ============================================================
# NOTIFICATION
# ============================================================

class Notification(Base):
    __tablename__ = "notification"

    id: Mapped[int] = mapped_column(
        BigInteger,
        primary_key=True,
        autoincrement=True
    )

    titre: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    type: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    lu: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False
    )

    utilisateur_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("utilisateur.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )

    utilisateur: Mapped["Utilisateur"] = relationship(
        "Utilisateur",
        back_populates="notifications"
    )