from flask import Flask, render_template, request
import psycopg2


#  Object Flask
app = Flask(__name__)


#  route to /
@app.route('/')
def home():
    return render_template('index.html')


#  route to /listarProfessores
@app.route('/listarProfessores')
def professorList():
    return render_template('listarProfessores.html',
                           professorsList=get_professors())


#  route to /exibirProfessor
@app.route('/exibirProfessor')
def exibirProfessor():
    return render_template('exibirProfessor.html',
                           professor_data=get_professor_data(
                               request.args.get('professor')),
                           disciplines=get_professor_disciplines(
                               request.args.get('professor'))
                           )


#  route to /ConsultarPorTitulacao
@app.route('/ConsultarPorTitulacao')
def consultaPorTitulacao():
    if request.args.get('titulacao') is None:
        return render_template('consultaTitulacao.html', titulacao=None)

    return render_template('consultaTitulacao.html',
                           titulacao=request.args.get('titulacao'),
                           result=get_professors_titulacao(
                               request.args.get('titulacao'))
                           )


#  route to /consultarApenasComputacao
@app.route('/consultarApenasComputacao')
def consultarApenasComputacao():
    return render_template('consultarApenasComputacao.html',
                    computationProfessors=get_computation_professors())


#  route to /calcularSalarioProfessor
@app.route('/calcularSalarioProfessor')
def calcularSalarioProfessor():
    return render_template('/calcularSalarioProfessor.html',
                           salario=get_salario_data(request.args.get('pk_professor')),
                           nome=request.args.get('nome')
                           )

"""****************************************************************************
**                    ACESSO AO BANCO DE DADOS E CONSULTAS                   **
****************************************************************************"""


def get_cursor():
    con = psycopg2.connect(host='localhost', database='Faculdade',
                           user='rafael', password='rafael123')
    return con.cursor()


def get_professors():
    # Gerando o cursor
    cur = get_cursor()

    # Executando a Busca
    cur.execute("""select nome, pk_professor from professor""")

    # Recuperando o retorno do BD
    professors = cur.fetchall()

    # Fechar o cursor
    cur.close()
    return professors


def get_professor_data(pk_professor):
    # Gerando o cursor
    cur = get_cursor()

    # Executando a Busca
    cur.execute(f"""select nome, data_nasc, nome_mae, titulacao, pk_professor from professor
    where pk_professor = {pk_professor}""")

    # Recuperando o retorno do BD
    professor_data = cur.fetchone()

    # Fechar o cursor
    cur.close()
    return professor_data


def get_professor_disciplines(pk_professor):
    # Gerando o cursor
    cur = get_cursor()

    # Executando a Busca
    cur.execute(f"""select nome from disciplina
        where fk_professor = {pk_professor}""")

    # Recuperando o retorno do BD
    professor_disciplines = cur.fetchall()

    # Fechar o cursor
    cur.close()
    return professor_disciplines


def get_professors_titulacao(titulacao):
    # Gerando o cursor
    cur = get_cursor()

    # Executando a Busca
    cur.execute(f"""select nome from professor
            where titulacao = {int(titulacao)}""")

    # Recuperando o retorno do BD
    professor_titulacao = cur.fetchall()

    # Fechar o cursor
    cur.close()
    return professor_titulacao


def get_computation_professors():
    # Gerando o cursor
    cur = get_cursor()

    # Executando a Busca
    cur.execute(
        f"""select nome from professor 
            where pk_professor IN (select fk_professor from disciplina where curso like 'Ciência da Computação')
              """)

    # Recuperando o retorno do BD
    computation_professor = cur.fetchall()

    # Fechar o cursor
    cur.close()
    return computation_professor


def get_salario_data(pk_professor):
    # Gerando o cursor
    cur = get_cursor()

    # Executando a Busca
    cur.execute(
        f"""select carga_horaria from disciplina 
            where fk_professor = {pk_professor}
              """)

    # Recuperando o retorno do BD
    carga = cur.fetchall()

    # Fechar o cursor
    cur.close()

    # Somando o retorno
    carga_horaria = 0
    for carga_curso in carga:
        carga_horaria += int(carga_curso[0])

    return carga_horaria * 50

#  start app
if __name__ == '__main__':
    app.run(debug=True)