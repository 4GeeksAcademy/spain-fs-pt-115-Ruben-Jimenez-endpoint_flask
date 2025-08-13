from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Column, Table, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

db = SQLAlchemy()

favorite_character = Table(
    "favorite_character",
    db.Model.metadata,
    Column("users_id", ForeignKey("users.id"), primary_key=True),
    Column("characters_id", ForeignKey("characters.id"), primary_key=True),
)
favorite_akatsuki = Table(
    "favorite_akatsuki",
    db.Model.metadata,
    Column("users_id", ForeignKey("users.id"), primary_key=True),
    Column("akatsuki_id", ForeignKey("akatsuki.id"), primary_key=True),
)
favorite_tailed_beasts = Table(
    "favorite_tailed_beasts",
    db.Model.metadata,
    Column("users_id", ForeignKey("users.id"), primary_key=True),
    Column("tailed_beasts_id", ForeignKey("tailed_beasts.id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120),unique=True, nullable=False)
    email: Mapped[str] = mapped_column( String(120), unique=True, nullable=False) 
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    characters: Mapped[List["Character"]] = relationship(secondary=favorite_character)
    
    akatsuki: Mapped[List["Akatsuki"]] = relationship(secondary=favorite_akatsuki)
    tailed_beasts: Mapped[List["TailedBeasts"]] = relationship(secondary=favorite_tailed_beasts)

   

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "favorites_characters": [c.serialize() for c in self.characters ],
            "favorites_akatsuki": [a.serialize()for a in self.akatsuki],
            "favortes_tailed_beast":[t.serialize()for t in self.tailed_beasts]
            # do not serialize the password, its a security breach
        }


class Character(db.Model):
    __tablename__ = "characters"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    img: Mapped[str] = mapped_column(String(255), nullable=False)
    sex: Mapped[str] = mapped_column(String(25), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "sex": self.sex
        }


class Akatsuki(db.Model):
    __tablename__ = "akatsuki"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    img: Mapped[str] = mapped_column(String(255), nullable=False)
    sex: Mapped[str] = mapped_column(String(25), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "sex": self.sex
        }


class TailedBeasts(db.Model):
    __tablename__ = "tailed_beasts"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    img: Mapped[str] = mapped_column(String(255), nullable=False)
    family: Mapped[str] = mapped_column(String(255), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "img": self.img,
            "family": self.family
        }