from flask import Flask,render_template,request
from flask_sqlalchemy import SQLAlchemy
import hashlib

app=Flask(__name__)
app.config.from_pyfile('config.py')

from models import db
from models import Usuario,Ingrediente,Receta

usuario=None

@app.route('/')
def Inicio():
    return render_template('inicio.html')

@app.route('/menu',methods=['POST','GET'])
def Menu():
    global usuario
    if request.method =='POST':
        if not request.form['email'] or not request.form['password']:
            return  render_template('inicio.html')
        else:
            usuario_actual=Usuario.query.filter_by(correo=request.form['email']).first()
            if usuario_actual == None:
                return render_template('inicio.html')
            else:
                if usuario_actual.clave == hashlib.md5(bytes(request.form['password'], encoding="utf-8")).hexdigest():
                    usuario = usuario_actual
                    return render_template('menu.html', persona=usuario_actual)
                else:
                    return render_template('inicio.html')
    else:
        #error
        return render_template("inicio.html")

@app.route('/ingresar',methods=['POST','GET'])
def IngresarReceta():
    pass

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