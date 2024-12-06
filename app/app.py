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

@APP.route('/explicacao/SELECT')
def select():
    return render_template('explicacaoSELECT.html')

@APP.route('/explicacao/WHERE')
def where():
    return render_template('Where_explicacao.html')

@APP.route('/explicacao/LIKE')
def like():
    return render_template('explicacaoLIKE.html')

@APP.route('/explicacao/Conjuntos')
def conjuntos():
    return render_template('Conjuntos_explicacao.html')

@APP.route('/explicacao/Funcoesdeagregacao')
def funcoes_de_agragacao():
    return render_template('Funcoes_de_agregacoes.html')

@APP.route('/explicacao/Case_explicacao')
def case():
    return render_template('Cases_explicacao.html')

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

@APP.route('/pergunta/2')
def pergunta2():
    return render_template('pergunta2.html')

@APP.route('/pergunta/4')
def pergunta4():
    return render_template('pergunta4.html')

@APP.route('/pergunta/5')
def pergunta5():
    return render_template('pergunta5.html')

@APP.route('/pergunta/7')
def pergunta7():
    return render_template('pergunta7.html')