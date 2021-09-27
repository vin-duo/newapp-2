from flask import Flask, render_template, redirect, url_for, request

#para o db 333
from flask_sqlalchemy import SQLAlchemy

#migrate 444
from flask_migrate import Migrate

#organizar 555
from forms import Criar_ensaio, Alfa

from MAIN_dosagem import Ensaio



#create a Flask Instance
app = Flask(__name__)

#para o form 222
app.config['SECRET_KEY'] = "you-will-never-know"
#para o db 333
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newapp.db'
db = SQLAlchemy(app)
#para migrate 444
migrate = Migrate(app, db)







    # ROTAS

@app.route('/')
@app.route('/home')
def home():
    ensaios_registrados = Ensaios.query.all()
    return render_template('home.html', ensaios_registrados=ensaios_registrados)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html')


@app.route('/criar', methods=['POST', 'GET'])
def criar():

    form = Criar_ensaio()
    if form.validate_on_submit():

        novo_ensaio = Ensaios(
        nome = form.nome.data,
        piloto = form.piloto.data,
        rico = form.rico.data,
        pobre = form.pobre.data,
        pesobrita = form.pesobrita.data,
        slump = form.slump.data)
        db.session.add(novo_ensaio)
        db.session.commit()

        return redirect('/home')
    return render_template('criar.html', form=form)


@app.route('/home/<int:id>')
def apagar_ensaio(id):
    apagar = Ensaios.query.get_or_404(id)

    try:
        db.session.delete(apagar)
        db.session.commit()
        return redirect('/home')

    except:
        "DEU ERRADO"


@app.route('/editar_ensaio/<int:id>', methods=['POST', 'GET'])
def editar_ensaio(id):

    form = Criar_ensaio()

    editar = Ensaios.query.get_or_404(id)
    
    if form.validate_on_submit():
        editar.nome = form.nome.data
        editar.piloto = form.piloto.data
        editar.rico = form.rico.data
        editar.pobre = form.pobre.data
#        editar.cp = form.cp.data
        editar.pesobrita = form.pesobrita.data
        editar.slump = form.slump.data
#        editar.umidade = form.umidade.data
        db.session.commit()
        return redirect('/home')
    return render_template('editar_ensaio.html', form=form, editar=editar)





@app.route('/dosagem/<int:id>', methods=['POST', 'GET'])
def dosagem(id):
    form = Alfa()

    ensaio_salvo = Ensaios.query.filter_by(id=id).first()
    dosagens_do_ensaio_salvo = ensaio_salvo.dosagem_piloto

    m = ensaio_salvo.piloto
#    cp = ensaio_salvo.cp
    pesobrita = ensaio_salvo.pesobrita
    slump = ensaio_salvo.slump
#    umidade = ensaio_salvo.umidade

    if dosagens_do_ensaio_salvo != []:
        contador = 0
        indice = 0
        for i in dosagens_do_ensaio_salvo:
            alfa = i.alfa

            if contador == 0:
                alfaantigo = 0
            else:
                alfaantigo = dosagens_do_ensaio_salvo[contador-1].alfa

            traco = Ensaio(
                m = m,
                alfa = alfa, 
                pesobrita = pesobrita,
                alfaantigo = alfaantigo)

            i.alfa = alfa
            i.c_unitario = traco.massas_unitarias()[0]
            i.a_unitario = traco.massas_unitarias()[1]
            i.b_unitario = traco.massas_unitarias()[2]

            i.c_massa = traco.massas_iniciais()[0]
            i.a_massa = traco.massas_iniciais()[1]
            i.b_massa = traco.massas_iniciais()[2]
            
            i.c_acr = traco.quantidades_adicionar()[0]
            i.a_acr = traco.quantidades_adicionar()[1]

            i.a_massa_umida = traco.umidade_agregado()[0]
            i.umidade_agregado = traco.umidade_agregado()[1]

            i.ensaio = ensaio_salvo
            i.indice = indice

            db.session.commit()
            contador = contador + 1
            indice = indice + 1

    if form.validate_on_submit():
        add_no_db = Dosagem_piloto(alfa=form.alfa.data, ensaio = ensaio_salvo)
        db.session.add(add_no_db)
        db.session.commit()
        return redirect ('/dosagem/{}'.format(id))
    return render_template("dosagem.html", form=form, id=id, dosagens_do_ensaio_salvo=dosagens_do_ensaio_salvo, m=m, slump=slump, pesobrita=pesobrita)





@app.route("/agua", methods=["POST"])
def update_agua():#o nome "valor_alfa" é o nome dado no html para um elemento na tabela do db. Quando cria uma linha no db, a tabela chama essa linha de "valor_alfa", que tem as propriedades "id", "alfa", "agua"......
    i_id = request.form.get("i_id")
    valor_agua_novo = request.form.get("valor_agua_novo")
    nova_agua = Dosagem_piloto.query.filter_by(id=i_id).first()
    nova_agua.agua = valor_agua_novo
    db.session.commit()
    a = nova_agua.ensaio.id
    return redirect("/dosagem/{}".format(a))



@app.route('/auxiliar/<int:id>', methods=['POST', 'GET'])
def dosagem_auxiliar(id):

    form = Alfa()
    ensaio_salvo = Ensaios.query.filter_by(id=id).first()

    m_rico = ensaio_salvo.rico
    m_pobre = ensaio_salvo.pobre
#    cp = ensaio_salvo.cp
    alfa = form.alfa.data
    pesobrita = ensaio_salvo.pesobrita
    slump = ensaio_salvo.slump

    if form.validate_on_submit():
        if ensaio_salvo.dosagem_rico == []:
            traco = Ensaio(
                m = m_rico,
                alfa = form.alfa.data, 
                pesobrita = pesobrita)

            add_no_db_rico = Dosagem_rico(
                alfa = form.alfa.data,
                c_unitario = traco.massas_unitarias()[0],
                a_unitario = traco.massas_unitarias()[1],
                b_unitario = traco.massas_unitarias()[2],
                
                c_massa = traco.massas_iniciais()[0],
                a_massa = traco.massas_iniciais()[1],
                b_massa = traco.massas_iniciais()[2],
                
                c_acr = traco.quantidades_adicionar()[0],
                a_acr = traco.quantidades_adicionar()[1],
                
                agua = 0,
                ensaio = ensaio_salvo)

            traco = Ensaio(
                m = m_pobre,
                alfa = form.alfa.data, 
                pesobrita = pesobrita)

            add_no_db_pobre = Dosagem_pobre(
                alfa = form.alfa.data,
                c_unitario = traco.massas_unitarias()[0],
                a_unitario = traco.massas_unitarias()[1],
                b_unitario = traco.massas_unitarias()[2],
                
                c_massa = traco.massas_iniciais()[0],
                a_massa = traco.massas_iniciais()[1],
                b_massa = traco.massas_iniciais()[2],
                
                c_acr = traco.quantidades_adicionar()[0],
                a_acr = traco.quantidades_adicionar()[1],
                
                agua = 0,
                ensaio = ensaio_salvo)

            db.session.add(add_no_db_rico)
            db.session.add(add_no_db_pobre)
            db.session.commit()

        else:
            rico_velho = ensaio_salvo.dosagem_rico[0]
            pobre_velho = ensaio_salvo.dosagem_pobre[0]
            db.session.delete(rico_velho)
            db.session.delete(pobre_velho)
            db.session.commit()

            traco = Ensaio(
                m = m_rico,
                alfa = form.alfa.data, 
                pesobrita = pesobrita)

            add_no_db_rico = Dosagem_rico(
                alfa = form.alfa.data,
                c_unitario = traco.massas_unitarias()[0],
                a_unitario = traco.massas_unitarias()[1],
                b_unitario = traco.massas_unitarias()[2],
                
                c_massa = traco.massas_iniciais()[0],
                a_massa = traco.massas_iniciais()[1],
                b_massa = traco.massas_iniciais()[2],
                
                c_acr = traco.quantidades_adicionar()[0],
                a_acr = traco.quantidades_adicionar()[1],
                
                agua = 0,
                ensaio = ensaio_salvo)

            traco = Ensaio(
                m = m_pobre,
                alfa = form.alfa.data, 
                pesobrita = pesobrita)

            add_no_db_pobre = Dosagem_pobre(
                alfa = form.alfa.data,
                c_unitario = traco.massas_unitarias()[0],
                a_unitario = traco.massas_unitarias()[1],
                b_unitario = traco.massas_unitarias()[2],
                
                c_massa = traco.massas_iniciais()[0],
                a_massa = traco.massas_iniciais()[1],
                b_massa = traco.massas_iniciais()[2],
                
                c_acr = traco.quantidades_adicionar()[0],
                a_acr = traco.quantidades_adicionar()[1],
                
                agua = 0,
                ensaio = ensaio_salvo)
            db.session.add(add_no_db_rico)
            db.session.add(add_no_db_pobre)
            db.session.commit()
        return redirect('/auxiliar/{}'.format(id))
    return render_template("auxiliar.html", form=form, ensaio_salvo=ensaio_salvo, id=id, m_rico=m_rico, m_pobre=m_pobre, slump=slump)





#acabou dosagem auxiliar

@app.route('/dosagem/delete/<int:id>')#esse id é da linha na tabela Dosagem_piloto
def delete(id):
    #linha da dosagem a ser deletara
    dosagem_deletada = Dosagem_piloto.query.filter_by(id=id).first()
    #id do ensaio que essa dosagem pertence (.ensaio é o backref pra achar o o elemento "pai")
    dosagem_deletada.ensaio.id

    db.session.delete(dosagem_deletada)
    db.session.commit()

    return redirect('/dosagem/{}'.format(dosagem_deletada.ensaio.id))



@app.route('/dosagem_auxiliar/delete/<int:id>')#esse id é da linha na tabela Dosagem_piloto
def delete_auxiliar(id):
    #linha da dosagem a ser deletara
    dosagem_deletada_rico = Dosagem_rico.query.filter_by(id=id).first()
    dosagem_deletada_pobre = Dosagem_pobre.query.filter_by(id=id).first()

    id_do_ensaio = dosagem_deletada_rico.ensaio.id

    #id do ensaio que essa dosagem pertence (.ensaio é o backref pra achar o o elemento "pai")
#    dosagem_deletada_pobre.ensaio.id
#    dosagem_deletada_pobre.ensaio.id

    db.session.delete(dosagem_deletada_rico)
    db.session.delete(dosagem_deletada_pobre)
    db.session.commit()

    return redirect('/auxiliar/{}'.format(id_do_ensaio))


@app.route('/resultados/<int:id>', methods=['POST', 'GET'])
def resultados(id):
#    form = Confirmar_dosagem()#Criar esse formulario
#    if form.validate_on_submit():
#        print('validou')
    return render_template('resultados.html', id=id)


@app.route('/corpo_de_prova/<int:id>', methods=['POST', 'GET'])
def corpo_de_prova(id):
#    form = Resistencia()#CRIAR O FORMULARIO DA RESISTENCIA IGUAL DO ALFA
#    if form.validate_on_submit():
#        pass

    ensaio_salvo = Ensaios.query.filter_by(id=id).first()
    cps_piloto = Cp_piloto.query.all()
    cps_rico = Cp_rico.query.all()
    cps_pobre = Cp_pobre.query.all()
    print('\nid')
    print(id)
    print(cps_piloto)
    print(cps_rico)
    print(cps_pobre)

    r_piloto = request.form.get("resistencia_piloto")
    r_rico = request.form.get("resistencia_rico")
    r_pobre = request.form.get("resistencia_pobre")

    if request.method == 'POST':

        if r_piloto != "":
            print('entrei piloto diferente de None')
#            print(r_piloto)
            cp_piloto = Cp_piloto(resistencia=r_piloto, ensaio=ensaio_salvo)
            db.session.add(cp_piloto)
            db.session.commit()
        if r_rico != "":
            print('entrei rico diferente de None')
#            print(r_rico)
#            print(type(r_rico))
            cp_rico = Cp_rico(resistencia=r_rico, ensaio=ensaio_salvo)
            db.session.add(cp_rico)
            db.session.commit()
        if r_pobre != "":
            print('entrei pobre diferente de None')
#            print(r_pobre)
            cp_pobre = Cp_pobre(resistencia=r_pobre, ensaio=ensaio_salvo)
            db.session.add(cp_pobre)
            db.session.commit()
        return redirect('/corpo_de_prova/{}'.format(id))
    return render_template('corpo_de_prova.html', id=id, cps_piloto=cps_piloto, cps_rico=cps_rico, cps_pobre=cps_pobre, ensaio_salvo=ensaio_salvo)


@app.route('/corpo_de_prova/deletar_piloto/<int:id>')
def deletar_corpo_de_prova_piloto(id):
    apagar = Cp_piloto.query.get_or_404(id)#CRIAR A TABELA DO CORPO DE PROVA
    print('apagar.ensaio.id')
    print(apagar.ensaio.id)

    try:
        db.session.delete(apagar)
        db.session.commit()
        return redirect('/corpo_de_prova/{}'.format(apagar.ensaio.id))
    except:
        "DEU ERRADO"


@app.route('/corpo_de_prova/deletar_rico/<int:id>')
def deletar_corpo_de_prova_rico(id):
    apagar = Cp_rico.query.get_or_404(id)#CRIAR A TABELA DO CORPO DE PROVA
    print('apagar.ensaio.id')
    print(apagar.ensaio.id)

    try:
        db.session.delete(apagar)
        db.session.commit()
        return redirect('/corpo_de_prova/{}'.format(apagar.ensaio.id))
    except:
        "DEU ERRADO"


@app.route('/corpo_de_prova/deletar_pobre/<int:id>')
def deletar_corpo_de_prova_pobre(id):
    apagar = Cp_pobre.query.get_or_404(id)#CRIAR A TABELA DO CORPO DE PROVA
    print('apagar.ensaio.id')
    print(apagar.ensaio.id)

    try:
        db.session.delete(apagar)
        db.session.commit()
        return redirect('/corpo_de_prova/{}'.format(apagar.ensaio.id))
    except:
        "DEU ERRADO"









    # MODELS 333

class Ensaios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(30))
    piloto = db.Column(db.Integer)
    rico = db.Column(db.Integer)
    pobre = db.Column(db.Integer)
    cp = db.Column(db.Integer)
    pesobrita = db.Column(db.Integer)
    slump = db.Column(db.Integer)
    umidade = db.Column(db.Integer)
    dosagem_piloto = db.relationship('Dosagem_piloto', backref='ensaio')
    dosagem_rico = db.relationship('Dosagem_rico', backref='ensaio')
    dosagem_pobre = db.relationship('Dosagem_pobre', backref='ensaio')
    cp_piloto = db.relationship('Cp_piloto', backref='ensaio')
    cp_rico = db.relationship('Cp_rico', backref='ensaio')
    cp_pobre = db.relationship('Cp_pobre', backref='ensaio')

    def __repr__(self):
        return '\n<id: {}, nome: {} piloto: {}, rico: {}, pobre: {}, cp: {}, pesobrita: {}, slump: {}, umidade: {}, relation {} >'.format(self.id, self.nome, self.piloto, self.rico, self.pobre, self.cp, self.pesobrita, self.slump, self.umidade, self.dosagem_piloto)


class Dosagem_piloto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alfa = db.Column(db.Integer)

    c_unitario = db.Column(db.Integer)
    a_unitario = db.Column(db.Integer)
    b_unitario = db.Column(db.Integer)
    
    c_massa = db.Column(db.Integer)
    a_massa = db.Column(db.Integer)

    b_massa = db.Column(db.Integer)
    
    c_acr = db.Column(db.Integer)
    a_acr= db.Column(db.Integer)

    a_massa_umida = db.Column(db.Integer)    
    umidade_agregado = db.Column(db.Integer)
    agua = db.Column(db.Integer)

    indice = db.Column(db.Integer)
    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

    def __repr__(self):
        return '\n<id: {}, Piloto: {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, foreign: {}>'.format(self.id, self.alfa, self.c_unitario, self.a_unitario, self.b_unitario, self.c_massa, self.a_massa, self.b_massa, self.c_acr, self.a_acr, self.a_massa_umida, self.umidade_agregado, self.agua, self.ensaio_id)
   

class Dosagem_rico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alfa = db.Column(db.Integer)

    c_unitario = db.Column(db.Integer)
    a_unitario = db.Column(db.Integer)
    b_unitario = db.Column(db.Integer)

    c_massa = db.Column(db.Integer)
    a_massa = db.Column(db.Integer)
    b_massa = db.Column(db.Integer)
    
    c_acr = db.Column(db.Integer)
    a_acr= db.Column(db.Integer)
    
    a_massa_umida = db.Column(db.Integer)    
    umidade_agregado = db.Column(db.Integer)
    agua = db.Column(db.Integer)

    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

    def __repr__(self):
        return '\n<id: {}, Rico: {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, foreign: {}>'.format(self.id, self.alfa, self.c_unitario, self.a_unitario, self.b_unitario, self.c_massa, self.a_massa, self.b_massa, self.a_massa_umida, self.c_acr, self.a_acr, self.a_massa_umida, self.umidade_agregado, self.agua, self.ensaio_id)
   

class Dosagem_pobre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    alfa = db.Column(db.Integer)

    c_unitario = db.Column(db.Integer)
    a_unitario = db.Column(db.Integer)
    b_unitario = db.Column(db.Integer)
    
    c_massa = db.Column(db.Integer)
    a_massa = db.Column(db.Integer)
    b_massa = db.Column(db.Integer)
    
    c_acr = db.Column(db.Integer)
    a_acr= db.Column(db.Integer)
    
    a_massa_umida = db.Column(db.Integer)
    umidade_agregado = db.Column(db.Integer)
    agua = db.Column(db.Integer)

    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

    def __repr__(self):
        return '\n<id: {}, Pobre: {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, foreign: {}>'.format(self.id, self.alfa, self.c_unitario, self.a_unitario, self.b_unitario, self.c_massa, self.a_massa, self.a_massa_umida, self.b_massa, self.c_acr, self.a_acr, self.a_massa_umida, self.umidade_agregado, self.agua, self.ensaio_id)


class Cp_piloto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resistencia = db.Column(db.Integer)
    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

    def __repr__(self):
        return '<id: {}, r: {} MPa, ensaio_id {}>'.format(self.id, self.resistencia, self.ensaio_id)


class Cp_rico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resistencia = db.Column(db.Integer)
    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

    def __repr__(self):
        return '<id: {}, r: {} MPa, ensaio_id {}>'.format(self.id, self.resistencia, self.ensaio_id)


class Cp_pobre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resistencia = db.Column(db.Integer)
    ensaio_id = db.Column(db.Integer, db.ForeignKey('ensaios.id'))

    def __repr__(self):
        return '<id: {}, r: {} MPa, ensaio_id {}>'.format(self.id, self.resistencia, self.ensaio_id)






















class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    pets = db.relationship('Pet', backref='owner')

class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    owner_id = db.Column(db.Integer, db.ForeignKey('person.id'))
