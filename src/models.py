from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Table, Column, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from eralchemy2 import render_er
from datetime import datetime

# Inicializar Flask-SQLAlchemy
db = SQLAlchemy()

# Una tabla User - Favorite → Uno-a-muchos (Un usuario puede tener muchos favoritos, pero cada favorito pertenece a un solo usuario).
# Una tabla User - Post     → Uno-a-muchos (Un usuario puede escribir varios posts, pero un post pertenece a un solo usuario).
# Una tabla Post - Comment  → Uno-a-muchos (Un post puede tener varios comentarios, pero cada comentario pertenece a un solo post).
# Una tabla User - Comment  → Uno-a-muchos (Un usuario puede hacer varios comentarios, pero cada comentario pertenece a un solo usuario).
# Una tabla Character/Planet/Vehicle - Favorite → Muchos-a-muchos (Un usuario puede guardar varios personajes, planetas o vehículos como favoritos y estos pueden ser favoritos de varios usuarios).

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    # Relaciones
    favorites = relationship("Favorite", back_populates="user")
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            # do not serialize the password, its a security breach
        }

class Character(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    birth_year: Mapped[str] = mapped_column(String(50), nullable=False)

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    climate: Mapped[str] = mapped_column(String(50), nullable=False)
    terrain: Mapped[str] = mapped_column(String(50), nullable=False)

class Vehicle(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    model: Mapped[str] = mapped_column(String(50), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(50), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)

class Favorite(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=True)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicle.id"), nullable=True)
    # Relaciones
    user: Mapped[list['User']] = relationship("User", back_populates="favorites")
    character: Mapped[list['Character']] = relationship("Character")
    planet: Mapped[list['Planet']] = relationship("Planet")
    vehicle: Mapped[list['Vehicle']] = relationship("Vehicle")

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(250), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    # Relaciones
    user: Mapped[list['User']] = relationship("User", back_populates="posts")
    comments: Mapped[list['Comment']] = relationship("Comment", back_populates="post")

class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    # Relaciones
    user: Mapped[list['User']] = relationship("User", back_populates="comments")
    post: Mapped[list['Post']] = relationship("Post", back_populates="comments")




    
   

