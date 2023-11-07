from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:senha_root@localhost/cadastro'
db = SQLAlchemy(app)

class Setor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primeiro_nome = db.Column(db.String(50), nullable=False)
    sobrenome = db.Column(db.String(50), nullable=False)
    data_admissao = db.Column(db.Date, nullable=False)
    status_funcionario = db.Column(db.Boolean, nullable=False)
    id_setor = db.Column(db.Integer, db.ForeignKey('setor.id'))
    setor = db.relationship('Setor', backref='funcionarios')
    cargo = db.Column(db.String(50), nullable=False)

class Cargo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    setor = db.relationship('Setor', backref='cargos')
    id_setor = db.Column(db.Integer, db.ForeignKey('setor.id'))


@app.route('/visualizar_dados')
def visualizar_dados():
    funcionarios = Funcionario.query.all()

    return render_template('visualizar_dados.html', funcionarios=funcionarios)


with app.app_context():
    db.create_all()

@app.route('/')
def formulario():
    return render_template('formulario.html')

@app.route('/salvar', methods=['POST'])
def salvar():
    if request.method == 'POST':
        setor_nome = request.form['setor_nome']
        funcionario_primeiro_nome = request.form['funcionario_primeiro_nome']
        funcionario_sobrenome = request.form['funcionario_sobrenome']
        funcionario_data_admissao = request.form['funcionario_data_admissao']
        status_funcionario = bool(request.form.get('funcionario_status')) 
        cargo_nome = request.form['cargo_nome']

        setor = Setor.query.filter_by(nome=setor_nome).first()

        if not setor:
            setor = Setor(nome=setor_nome)
        

        funcionarios = Funcionario(
            primeiro_nome=funcionario_primeiro_nome,
            sobrenome=funcionario_sobrenome,
            data_admissao=funcionario_data_admissao,
            status_funcionario=status_funcionario, 
            setor=setor,
            id_setor = setor.id,
            cargo = cargo_nome
        )
        cargos = Cargo(
            nome=cargo_nome,
            setor=setor,
            id_setor = setor.id
        )

        db.session.add(setor)
        db.session.add(funcionarios)
        db.session.add(cargos)
        db.session.commit()
        return redirect(url_for('formulario'))

if __name__ == '__main__':
    app.run(debug=True)
