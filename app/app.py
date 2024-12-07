import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from flask import render_template, Flask, request
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

# DIOGO
@APP.route('/AlunosMatriculados', methods=['GET', 'POST'])
def visualizarDados():
    concelhos = db.execute('SELECT DISTINCT concelho FROM Concelhos').fetchall()
    distritos = db.execute('SELECT DISTINCT distrito FROM Distritos').fetchall()

    # Recupera os valores dos filtros
    selected_concelho = request.form.get('concelho')
    selected_distrito = request.form.get('distrito')
    selected_escola = request.form.get('escola')
    selected_n_homens_min = request.form.get('n_homens_min', type=int) or 0
    selected_n_homens_max = request.form.get('n_homens_max', type=int) or 500
    selected_n_mulheres_min = request.form.get('n_mulheres_min', type=int) or 0
    selected_n_mulheres_max = request.form.get('n_mulheres_max', type=int) or 500
    selected_ordenacao = request.form.get('ordenacao')

    # Base da query
    query = '''
        WITH tabela AS (
            SELECT 
                   ESCOLAS.COD as codEscola,
                   ESCOLAS.ESCOLA AS Escola,
                   AGRUPAMENTOS.COD as codAgrupamento,
                   AGRUPAMENTOS.AGRUPAMENTO as Agrupamento, 
                   SUM(CASE WHEN ALUNOS.SEXO = 'Mulheres' THEN ALUNOS.quantidade ELSE 0 END) as "n_mulheres",
                   SUM(CASE WHEN ALUNOS.SEXO = 'Homens' THEN ALUNOS.quantidade ELSE 0 END) as "n_homens",
                   CONCELHOS.CONCELHO as Concelho,
                   DISTRITOS.DISTRITO as Distrito,
                   DISTRITOS.COD as codDistrito,
                   CONCELHOS.COD as codConcelho
            FROM ESCOLAS
            JOIN TURMAS ON ESCOLAS.COD = TURMAS.escola
            JOIN ALUNOS ON TURMAS.COD = ALUNOS.TURMA
            JOIN CONCELHOS ON ESCOLAS.CONCELHO = CONCELHOS.COD
            JOIN DISTRITOS ON CONCELHOS.DISTRITO = DISTRITOS.COD
            LEFT JOIN AGRUPAMENTOS ON ESCOLAS.AGRUPAMENTO = AGRUPAMENTOS.COD
            GROUP BY ESCOLAS.COD
        )
        SELECT * FROM tabela WHERE 1=1
    '''

    # Adiciona filtros dinamicamente
    params = {}
    if selected_concelho:
        query += ' AND tabela.Concelho = :selected_concelho'
        params['selected_concelho'] = selected_concelho
    if selected_distrito:
        query += ' AND tabela.Distrito = :selected_distrito'
        params['selected_distrito'] = selected_distrito
    if selected_escola:
        query += ' AND tabela.Escola LIKE :selected_escola'
        params['selected_escola'] = f"%{selected_escola}%"
    if selected_n_homens_min is not None:
        query += ' AND tabela.n_homens >= :selected_n_homens_min'
        params['selected_n_homens_min'] = selected_n_homens_min
    if selected_n_homens_max is not None:
        query += ' AND tabela.n_homens <= :selected_n_homens_max'
        params['selected_n_homens_max'] = selected_n_homens_max
    if selected_n_mulheres_min is not None:
        query += ' AND tabela.n_mulheres >= :selected_n_mulheres_min'
        params['selected_n_mulheres_min'] = selected_n_mulheres_min
    if selected_n_mulheres_max is not None:
        query += ' AND tabela.n_mulheres <= :selected_n_mulheres_max'
        params['selected_n_mulheres_max'] = selected_n_mulheres_max

    # Adiciona ordenação
    if selected_ordenacao:
        column, order = selected_ordenacao.rsplit('_', 1)
        query += f' ORDER BY tabela.{column} {order.upper()}'

    # Limita os resultados
    query += ' LIMIT 50'

    # Executa a query
    tabela = db.execute(query, params).fetchall()

    # Renderiza a página com os resultados
    return render_template(
        'visualizarDados.html',
        tabela=tabela,
        concelhos=concelhos,
        distritos=distritos,
        selected_concelho=selected_concelho,
        selected_distrito=selected_distrito,
        selected_escola=selected_escola,
        selected_n_homens_min=selected_n_homens_min,
        selected_n_homens_max=selected_n_homens_max,
        selected_n_mulheres_min=selected_n_mulheres_min,
        selected_n_mulheres_max=selected_n_mulheres_max,
        selected_ordenacao=selected_ordenacao
    )

@APP.route('/escolas/<int:cod>/')
def visualizarTurmasdaEscola(cod):
    escolaX = db.execute('''
            SELECT 
                entidades.entidade as ENTIDADE,
                escolas.cod as CODIGO,
                escolas.escola as ESCOLA,
                agrupamentos.cod as CODAGRUPAMENTO,
                agrupamentos.agrupamento as AGRUPAMENTO,
                concelhos.cod as CODCONCELHO,
                concelhos.concelho as CONCELHO,
                distritos.cod as CODDISTRITO,
                distritos.distrito as DISTRITO,
                turmas.cod as CODIGOTURMA,
                turmas.nivel as NIVEL,
                turmas.ciclo as CICLO,
                turmas.ano as ANO     
            FROM escolas
            JOIN entidades ON escolas.entidade = entidades.cod
            JOIN turmas ON escolas.cod = turmas.escola
            LEFT JOIN agrupamentos ON agrupamentos.cod = escolas.agrupamento
            JOIN concelhos ON concelhos.cod = escolas.concelho
            JOIN distritos ON distritos.cod = concelhos.distrito
            WHERE escolas.cod = ? ''', (cod,)).fetchall()
    return render_template('turmasDaEscola.html', escolaX=escolaX)

@APP.route('/escolas/<int:cod>/turmas/<int:codTurma>/')
def visualizarAlunosdaTurma(cod,codTurma):
    turmaX = db.execute('''
        SELECT
            escolas.escola as ESCOLA,
            turmas.cod as CODTURMA,
            turmas.natureza as NATUREZA,
            turmas.orientacao as ORIENTACAO,
            turmas.nivel as NIVEL,
            turmas.oferta as OFERTA,
            turmas.ano as ANO,
            turmas.ciclo as CICLO,
            turmas.curso as CURSO,
            SUM(CASE WHEN ALUNOS.SEXO = 'Mulheres' THEN ALUNOS.quantidade ELSE 0 END) as "n_mulheres",
            SUM(CASE WHEN ALUNOS.SEXO = 'Homens' THEN ALUNOS.quantidade ELSE 0 END) as "n_homens"
        from turmas 
        JOIN escolas ON escolas.cod = turmas.escola
        JOIN alunos on turmas.cod = alunos.turma
        where turmas.cod = ? and escolas.cod = ?''', (codTurma,cod)).fetchone()
    print(codTurma)
    return render_template('alunosDaTurma.html', turmaX=turmaX)

@APP.route('/distritos/<int:codDistrito>/')
def visualizarConcelhosNoDistrito(codDistrito):
    distritoX = db.execute('''
        SELECT 
            concelhos.cod AS CODIGO,
            concelhos.concelho AS CONCELHO,
            distritos.distrito AS DISTRITO,
            distritos.cod AS CODDISTRITO,
            COUNT(concelhos.cod) OVER (PARTITION BY distritos.cod) AS N_CONCELHOS
        FROM concelhos
        JOIN distritos ON concelhos.distrito = distritos.cod
        WHERE distritos.cod = ?''', (codDistrito,)).fetchall()
    return render_template('concelhosNoDistrito.html', distritoX = distritoX)

@APP.route('/concelhos/<int:codConcelho>/')
def visualizarEscolasNoConcelho(codConcelho):
    concelhoX = db.execute('''
        SELECT 
            escolas.cod AS CODIGOESCOLA,
            escolas.escola AS ESCOLA,
            concelhos.concelho AS CONCELHO,
            concelhos.cod AS CODCONCELHO,
            COUNT(escolas.cod) OVER (PARTITION BY concelhos.cod) AS N_ESCOLAS
        FROM escolas
        JOIN concelhos ON escolas.concelho = concelhos.cod
        WHERE concelhos.cod = ? ''', (codConcelho,)).fetchall()
    return render_template('escolasNoConcelho.html', concelhoX = concelhoX)

@APP.route('/agrupamentos/<int:codAgrupamento>/')
def visualizarEscolasNoAgrupamento(codAgrupamento):
    agrupamentoX = db.execute('''
        select 
            agrupamentos.cod as CODAGRUPAMENTO, 
            agrupamentos.agrupamento as AGRUPAMENTO,
            escolas.cod as CODESCOLA,
            escolas.escola as ESCOLA,
            agrupamentos.codSede as CODSEDE,
            (select escolas.escola from escolas where cod = agrupamentos.codSede) as ESCOLASEDE,
            (select COUNT(*) from escolas where escolas.agrupamento = ?) as N_ESCOLAS
        from escolas
        JOIN agrupamentos ON agrupamentos.cod = escolas.agrupamento
        where agrupamentos.cod = ?''', (codAgrupamento, codAgrupamento,)).fetchall()
    return render_template('escolasNoAgrupamento.html', agrupamentoX = agrupamentoX)