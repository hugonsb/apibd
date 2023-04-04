import psycopg2
from datetime import datetime
from flask import Flask, jsonify, request

api = Flask(__name__)

# Conecta ao banco de dados PostgreSQL
banco = psycopg2.connect(
        host="projetobd.cpq0d6o4wlxw.us-east-1.rds.amazonaws.com",
        database="projetobd",
        user="postgres",
        password="alunoaluno"
)

class User:
    def __init__(self, cpf, nome, data_nascimento):
        self.cpf = cpf
        self.nome = nome
        self.data_nascimento = data_nascimento

    def get_cpf(self):
        return self.cpf

    def set_cpf(self, cpf):
        self.cpf = cpf

    def get_nome(self):
        return self.nome

    def set_nome(self, nome):
        self.nome = nome

    def get_data_nascimento(self):
        return self.data_nascimento

    def set_data_nascimento(self, data_nascimento):
        self.data_nascimento = data_nascimento


def get_user(cpf):

    try:
        # Busca o usuário no banco de dados
        comando = banco.cursor()
        banco.rollback()
        comando.execute("SELECT * FROM banco.usuario WHERE cpf = " + str(cpf))
        results = comando.fetchall()

        if results:
            return results
        else:
            return "Usuario nao encontrado"

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return str (error)


#criar um novo usuário
def create_user(cpf, nome, data_nascimento):
    user = User(cpf, nome, data_nascimento)
    formato = "%Y-%m-%d"
    data_hora = datetime.strptime(user.get_data_nascimento(), formato)

    try:
        comando = banco.cursor()
        banco.rollback()

        comando.execute("INSERT INTO banco.usuario VALUES ((CAST (%s AS INTEGER)),%s,%s)", (user.get_cpf(), user.get_nome(), data_hora))
        banco.commit()
        return 'Usuário criado com sucesso!'

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return str (error)

#consultar usuario por cpf
@api.route('/usuario/<int:cpf>', methods=['GET'])
def obterUsuario(cpf):
    return jsonify(get_user(cpf))

#cadastrar usuario
@api.route('/criar_usuario', methods=['POST'])
def cadastrarUsuario():

    dados = request.get_json()
    cpf = dados['cpf']
    nome = dados['usuario']
    data_nascimento = dados['data_nascimento']

    result = create_user(cpf, nome, data_nascimento)

    return jsonify(str (result))

api.run(port=5000, host='localhost', debug=True)

#fechando conexao com bd
comando.close()
banco.close()