import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from flask import render_template, Flask
import logging
import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    stats = db.execute('''
        SELECT * FROM
            (SELECT COUNT(*) n_distritos FROM distritos)
        JOIN
            (SELECT COUNT(*) n_concelhos FROM concelhos)
    ''').fetchone()

    return render_template('index.html',stats=stats)

@APP.route('/explicacao/Where')
def where():
    return render_template('Where_explicacao.html')

@APP.route('/explicacao/Conjuntos')
def conjuntos():
    return render_template('Conjuntos_explicacao.html')

@APP.route('/explicacao/Funcoesdeagregacao')
def funcoes_de_agragacao():
    return render_template('Funcoes_de_agregacoes.html')

@APP.route('/explicacao/Case_explicacao')
def case():
    return render_template('Cases_explicacao.html')

@APP.route('/distritos/')
def listar_distritos():
    distritos = db.execute('''
        SELECT distritos.cod, distritos.designacao, COUNT(*) num_concelhos
        FROM distritos 
        JOIN concelhos ON concelhos.distrito = distritos.cod
        GROUP BY distritos.cod
        ORDER BY distritos.cod
    ''').fetchall()
    return render_template('listar_distritos.html', distritos=distritos)

@APP.route('/distritos/<int:codigo>/')
def distrito(codigo):
    # Obtém dados do distrito
    distrito = db.execute('''
        SELECT designacao
        FROM distritos 
        WHERE cod = ?
    ''', [codigo]).fetchone()
    # Obtém concelhos no distrito
    concelhos = db.execute('''
        SELECT cod, designacao
        FROM concelhos WHERE distrito = ?
        ORDER BY cod
    ''', [codigo]).fetchall()
    return render_template('distrito.html', 
                            distrito=distrito,
                            concelhos=concelhos)

@APP.route('/concelhos/')
def listar_concelhos():
    concelhos = db. execute("""
        SELECT concelhos.cod, concelhos.designacao, count(*) as num_recintos
            from concelhos 
            join recintos
            on concelhos.cod= recintos.concelho 
            group by concelhos.cod 
            order by concelhos.cod           
                             """).fetchall()
    return render_template('concelhos.html', concelhos=concelhos)
    



