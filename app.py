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
        SELECT cod, designacao
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

# DIOGO

@APP.route('/explicacao/SELECT')
def explicacaoSELECT():
    return render_template('explicacaoSELECT.html')

@APP.route('/explicacao/CompStrings')
def explicacaoLIKE():
    return render_template('explicacaoCompStrings.html')

@APP.route('/explicacao/SUBQUERY')
def explicacaoSUBQUERY():
    return render_template('explicacaoSUBQUERY.html')

@APP.route('/explicacao/SubperguntaVariavel')
def explicacaoSUBQUERYvarivavel():
    return render_template('explicacaoSubperguntaVariavel.html')