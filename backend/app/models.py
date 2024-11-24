from app import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50), unique=True, nullable=False)  # Especificar longitud
    contrasena = Column(String(50), nullable=False)  # Especificar longitud

class Libro(db.Model):
    __tablename__ = 'libros'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    titulo = Column(String(100), nullable=False)  # Especificar longitud
    autor = Column(String(100), nullable=False)  # Especificar longitud
    anyo_publicacion = Column(Integer)
    disponible = Column(Integer)  # Utilizar disponible en lugar de existencias

class Prestamo(db.Model):
    __tablename__ = 'prestamos'
    __table_args__ = {'extend_existing': True}
    id = Column(Integer, primary_key=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    libro_id = Column(Integer, ForeignKey('libros.id'), nullable=False)
    fecha_prestamo = Column(DateTime, default=datetime.utcnow)
    fecha_devolucion = Column(DateTime)

    usuario = relationship('Usuario')
    libro = relationship('Libro')
