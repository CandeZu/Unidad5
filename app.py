from functools import reduce
from tkinter import Menu
from tkinter.messagebox import RETRY
from unittest import removeResult
from flask import Flask, redirect,render_template,request, session,url_for
from flask_sqlalchemy import SQLAlchemy
import hashlib
from datetime import datetime

app=Flask(__name__)
app.config.from_pyfile('config.py')

from models import db
from models import Usuario,Ingrediente,Receta

usuario=None

@app.route('/IniciarSesion')
def Inicio():
    global usuario
    usuario=None
    return render_template('inicio.html')

@app.route('/',methods=['POST','GET'])
def Ingreso():
    global usuario
    if usuario == None:
        if request.method =='POST':
            if not request.form['email'] or not request.form['password']:
                return  render_template('error.html',mensaje='Debe ingresar los datos')
            else:
                usuario_actual=Usuario.query.filter_by(correo=request.form['email']).first()
                if usuario_actual == None:
                    return render_template('error.html',mensaje='No se encontró el usuario')
                else:
                    if usuario_actual.clave == hashlib.md5(bytes(request.form['password'], encoding="utf-8")).hexdigest():
                        usuario = usuario_actual
                        return render_template('menu.html',persona=usuario_actual)
                    else:
                        return render_template('error.html',mensaje='Contraseña Incorrecta')
        else:
            return redirect(url_for('Inicio'))
    else:
        return render_template('menu.html',persona=usuario)

@app.route('/ingresar_receta',methods=['POST','GET'])
def IngresarReceta():
    if usuario != None:
        if request.method == 'POST':
            if not request.form['nombre'] or not request.form['descripcion'] or not request.form['tiempo']:
                return redirect(url_for('IngresarReceta'))
            else:
                unaReceta=Receta(nombre=request.form['nombre'],tiempo=request.form['tiempo'],fecha=datetime.now(),elaboracion=request.form['descripcion'],cantidadmegusta=0,usuarioid=usuario.id)
                db.session.add(unaReceta)
                db.session.commit()
                return render_template('ingresar_ingredientes.html',id=unaReceta.id,nombre=unaReceta.nombre,numero=1)
        else:
            return render_template('ingresar_receta.html')
    else:
        return redirect(url_for("Inicio"))


@app.route('/agregar/<id>/<nombre>/<numero>', methods=['POST','GET'])
def AgregarIngrediente(id,nombre,numero):
    numero=int(numero)
    if usuario is not None:
        if request.method == 'POST':
            if not request.form['nombre1'] or not request.form['cantidad'] or not request.form['unidad']:
                return render_template('ingresar_ingredientes.html',id=id,nombre=nombre,numero=numero-1)
            else:
                if numero <=10:
                    unIngrediente=Ingrediente(nombre=request.form['nombre1'],cantidad=request.form['cantidad'],unidad=request.form['unidad'],recetaid=id)
                    db.session.add(unIngrediente)
                    db.session.commit()
                    return render_template('ingresar_ingredientes.html',id=id,nombre=nombre,numero=numero)
                else:
                    return redirect(url_for('RecetaAgregada',nombre=nombre))
        else:
            return render_template('ingresar_ingredientes.html',id=id,nombre=nombre,numero=numero)
    else:
        return redirect(url_for('Inicio'))

@app.route('/receta_agregada/<nombre>', methods=['POST','GET'])
def RecetaAgregada(nombre):
    if usuario != None:
        return render_template('receta_agregada.html',nombre=nombre)
    else:
        return redirect(url_for('Inicio'))

@app.route('/ranking',methods=['POST','GET'])
def Ranking():
    if usuario != None:
        lista:list = Receta.query.all()
        lista.sort(key=lambda receta:receta.cantidadmegusta)
        lista = lista[0:5]
        return render_template("mostrar_recetas.html", recetas=lista,titulo='Ranking')
    else:
        return redirect(url_for("Inicio"))


@app.route('/consultar_tiempo',methods=['POST','GET'])
def ConsultarPorTiempo():
    pass

@app.route('/consultar_ingrediente',methods=['POST','GET'])
def ConsultarPorIngrediente():
    pass

if __name__ == '__main__':
    app.run(debug=True)