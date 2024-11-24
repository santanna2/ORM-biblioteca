from flask import render_template, request, redirect, url_for, session, flash
from app import app, db
from app.forms import RegistroForm, LoginForm
from app.models import Usuario, Libro, Prestamo
from sqlalchemy.exc import IntegrityError
from datetime import datetime

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        nuevo_usuario = Usuario(nombre=form.nombre.data, contrasena=form.contrasena.data)
        try:
            db.session.add(nuevo_usuario)
            db.session.commit()
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            flash("El nombre de usuario ya está en uso. Por favor, elige otro.")
    return render_template('registro.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(nombre=form.nombre.data, contrasena=form.contrasena.data).first()
        if usuario:
            session['usuario_id'] = usuario.id  # Guardar el id del usuario en la sesión
            return redirect(url_for('ver_libros', usuario_id=usuario.id))
        else:
            flash("Nombre de usuario o contraseña incorrectos.")
    return render_template('login.html', form=form)

@app.route('/salir')
def salir():
    session.pop('usuario_id', None)  # Eliminar el id del usuario de la sesión
    return redirect(url_for('login'))

@app.route('/eliminar_usuario/<int:usuario_id>', methods=['POST'])
def eliminar_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    prestamos_pendientes = Prestamo.query.filter_by(usuario_id=usuario.id, fecha_devolucion=None).count()
    if prestamos_pendientes > 0:
        flash("No se puede eliminar el usuario porque tiene préstamos pendientes.")
        return redirect(url_for('mis_prestamos', usuario_id=usuario.id))
    else:
        prestamos = Prestamo.query.filter_by(usuario_id=usuario.id).all()
        for prestamo in prestamos:
            db.session.delete(prestamo)  # Eliminar todos los préstamos asociados al usuario
        db.session.delete(usuario)
        db.session.commit()
        session.pop('usuario_id', None)  # Eliminar el id del usuario de la sesión después de eliminar el usuario
        flash("Usuario eliminado exitosamente.")
        return redirect(url_for('home'))

@app.route('/libros/<int:usuario_id>', methods=['GET', 'POST'])
def ver_libros(usuario_id):
    if request.method == 'POST':
        termino_busqueda = request.form.get('termino_busqueda')
        libros = Libro.query.filter(Libro.titulo.ilike(f'%{termino_busqueda}%')).all()  # Búsqueda por nombre
    else:
        libros = Libro.query.all()
    return render_template('libros.html', libros=libros, usuario_id=usuario_id)

@app.route('/pedir_libro/<int:usuario_id>/<int:libro_id>', methods=['POST'])
def pedir_libro(usuario_id, libro_id):
    libro = Libro.query.get_or_404(libro_id)
    if libro.disponible > 0:
        libro.disponible -= 1
        nuevo_prestamo = Prestamo(usuario_id=usuario_id, libro_id=libro_id)
        db.session.add(nuevo_prestamo)
        db.session.commit()
    return redirect(url_for('ver_libros', usuario_id=usuario_id))

@app.route('/devolver_libro/<int:usuario_id>/<int:libro_id>', methods=['POST'])
def devolver_libro(usuario_id, libro_id):
    prestamo = Prestamo.query.filter_by(usuario_id=usuario_id, libro_id=libro_id, fecha_devolucion=None).first_or_404()
    prestamo.fecha_devolucion = datetime.utcnow()
    libro = Libro.query.get_or_404(libro_id)
    libro.disponible += 1
    db.session.commit()
    flash("Libro devuelto exitosamente.")
    return redirect(url_for('mis_prestamos', usuario_id=usuario_id))

@app.route('/mis_prestamos/<int:usuario_id>')
def mis_prestamos(usuario_id):
    prestamos = Prestamo.query.filter_by(usuario_id=usuario_id, fecha_devolucion=None).all()
    return render_template('mis_prestamos.html', prestamos=prestamos, usuario_id=usuario_id)
