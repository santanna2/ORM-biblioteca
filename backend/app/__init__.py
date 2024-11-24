from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="../../frontend/templates", static_folder="../../frontend/static")
app.config.from_object('config.Config')
db = SQLAlchemy(app)

from app import routes
from app.models import Usuario, Libro, Prestamo

with app.app_context():
    # Crear todas las tablas definidas en los modelos
    db.create_all()
    db.session.commit()

    # Insertar datos iniciales en la tabla de libros si no existen
    if Libro.query.count() == 0:
        libro1 = Libro(titulo="El Quijote", autor="Miguel de Cervantes", anyo_publicacion=1605, disponible=10)
        libro2 = Libro(titulo="Cien años de soledad", autor="Gabriel García Márquez", anyo_publicacion=1967, disponible=8)
        libro3 = Libro(titulo="1984", autor="George Orwell", anyo_publicacion=1949, disponible=7)
        libro4 = Libro(titulo="La Odisea", autor="Homero", anyo_publicacion=-800, disponible=5)
        db.session.add_all([libro1, libro2, libro3, libro4])
        db.session.commit()
