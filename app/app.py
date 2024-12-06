import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from flask import render_template, Flask
import logging
import db

APP = Flask(__name__)

# Start page
@APP.route('/')
def index():
    return render_template('index.html')



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

@APP.route('/perguntas/02')
def explicacao():
    return render_template('Resposta_2.html')

@APP.route('/explicacao/ORDER_BY')
def orderby():
    return render_template('explicacaoORDERBY.html')

@APP.route('/explicacao/JOIN')
def join():
    return render_template('explicacaoJOIN.html')

@APP.route('/explicacao/Agregacao_Dupla')
def agregacaoDupla():
    return render_template('explicacaoAgregacaoDupla.html')

@APP.route('/explicacao/row_number')
def rowNumber():
    return render_template('explicacaoRowNumber.html')

@APP.route('/pergunta/1')
def pergunta1():
    return render_template('pergunta1.html')

@APP.route('/pergunta/4')
def pergunta4():
    return render_template('pergunta4.html')

@APP.route('/pergunta/7')
def pergunta7():
    return render_template('pergunta7.html')


@APP.route('/distritos/')
def listar_distritos():
    distritos = db.execute('''
        SELECT distritos.cod, distritos.distrito, COUNT(*) num_concelhos
        FROM distritos 
        JOIN concelhos ON concelhos.distrito = distritos.cod
        GROUP BY distritos.cod
        ORDER BY distritos.cod
    ''').fetchall()
    return render_template('listar_distritos.html', distritos=distritos)

@APP.route('/concelhos/')
def listar_concelhos():
    concelhos = db.execute('''
        SELECT concelhos.cod, concelhos.concelho, COUNT(*) num_escolas, distritos.distrito
        FROM concelhos
        JOIN distritos ON distritos.cod = concelhos.distrito
        JOIN escolas ON escolas.concelho = concelhos.cod
        GROUP BY concelhos.cod
        ORDER BY concelhos.cod
    ''').fetchall()
    return render_template('listar_concelhos.html', concelhos=concelhos)

@APP.route('/escolas/')
def listar_escolas():
    escolas = db.execute('''
        SELECT escolas.cod, escolas.escola, count() as num_turmas, concelhos.concelho
        FROM escolas
        JOIN concelhos ON concelhos.cod = escolas.concelho
        JOIN distritos ON distritos.cod = concelhos.distrito
        JOIN turmas ON turmas.escola = escolas.cod
        GROUP BY escolas.cod
        ORDER BY escolas.cod
    ''').fetchall()
    return render_template('listar_escolas.html', escolas=escolas)