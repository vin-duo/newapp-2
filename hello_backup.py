from flask import Flask, render_template

#para os forms 222
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired

#para o db 333
from flask_sqlalchemy import SQLAlchemy

#migrate 444
from flask_migrate import Migrate


#create a Flask Instance
app = Flask(__name__)

#para o form 222
app.config['SECRET_KEY'] = "you-will-never-know"
#para o db 333
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newapp.db'
db = SQLAlchemy(app)
#para migrate 444
migrate = Migrate(app, db)


    # MODELS 333
    
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    def __repr__(self):
        return '<id(s): {}, name: {}'.format(self.id, self.name)





    # ROTAS

@app.route('/')
def index():
    favorite_pizza = ['primeiro', 'segundo', 'terceiro']
    return render_template('index.html', favorite_pizza= favorite_pizza)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html')


@app.route('/criar', methods=['POST', 'GET'])
def criar():
    alfa = None
    lista_de_alfa = []
    form = Alfa()
    if form.validate_on_submit():
        alfa = form.alfa.data
        lista_de_alfa.append(alfa)
        print(lista_de_alfa)
    return render_template('criar.html', form=form, alfa=alfa)




    # FORMS

class Alfa(FlaskForm):
    alfa = FloatField('Alfa:')
    submit = SubmitField('Registrar')

