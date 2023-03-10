from flask import Flask 
from flask import redirect
from flask import request
from flask import url_for
from flask import render_template

from flask import jsonify
from config import DevelopmentConfig
from flask_wtf.csrf import CSRFProtect
from models import db
from models import Alumnos

import forms 

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
csrf = CSRFProtect()

@app.route("/", methods=['GET', 'POST'])
def index():
    create_form = forms.UserForm(request.form)
    if request.method == 'POST':
        alum = Alumnos(nombre = create_form.nombre.data,
                       apellidos = create_form.nombre.data,
                       email = create_form.email.data
        )
        # Insert en la BD
        db.session.add(alum)
        db.session.commit()
    return render_template('index.html', form = create_form)

@app.route("/ABCompleto", methods=['GET', 'POST'])
def ABCompleto():
    create_form = forms.UserForm(request.form)
    # Select * from alumnos
    alumnos = Alumnos.query.all()
    return render_template('ABCompleto.html', form=create_form, alumnos=alumnos)

@app.route("/modificar", methods=['GET', 'POST'])
def modificar():
    create_form = forms.UserForm(request.form)
    if request.method=='GET':
        id = request.args.get('id')
        # Select * from alumnos where id==id    
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        create_form.id.data=alum1.id
        create_form.nombre.data=alum1.nombre
        create_form.apellidos.data=alum1.apellidos
        create_form.email.data=alum1.email

    if request.method=='POST':
        id = create_form.id.data
        # Select * from alumnos where id==id    
        alum=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        alum.nombre = create_form.nombre.data
        alum.apellidos = create_form.apellidos.data
        alum.email = create_form.email.data
        db.session.add(alum)
        db.session.commit()
        return redirect(url_for('ABCompleto'))
    return render_template('modificar.html', form=create_form)

@app.route("/eliminar", methods=['GET', 'POST'])
def eliminar():
    create_form = forms.UserForm(request.form)
    if request.method=='GET':
        id = request.args.get('id')
        # Select * from alumnos where id==id    
        alum1=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        create_form.id.data=alum1.id
        create_form.nombre.data=alum1.nombre
        create_form.apellidos.data=alum1.apellidos
        create_form.email.data=alum1.email

    if request.method=='POST':
        id = create_form.id.data
        # Select * from alumnos where id==id    
        alum=db.session.query(Alumnos).filter(Alumnos.id==id).first()
        db.session.delete(alum)
        db.session.commit()
        return redirect(url_for('ABCompleto'))
    return render_template('eliminar.html', form=create_form)


if __name__ == '__main__':
    # Aplicar la seguridad CSRF al inicializar la aplicaci??n
    csrf.init_app(app)
    # Objeto para la manipulaci??n de la BD
    db.init_app(app)
    # Comprueba si la BD existe y genera un mapeo en autom??tico de las tablas
    with app.app_context():
        db.create_all()
    app.run(port=3000)