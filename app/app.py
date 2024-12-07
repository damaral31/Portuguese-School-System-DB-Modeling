import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
from flask import render_template, Flask, request
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
    resposta = db.execute('''
    SELECT
        concelhos.concelho as concelho,
        COUNT(escolas.cod) as num
    FROM concelhos
    JOIN escolas ON escolas.concelho = concelhos.cod
    LEFT JOIN agrupamentos ON agrupamentos.cod = escolas.agrupamento
    WHERE agrupamentos.cod IS NULL
    GROUP BY concelhos.cod;
    ''').fetchall()
    return render_template('pergunta1.html', resposta=resposta)

@APP.route('/pergunta/2')
def pergunta2():
    resposta = db.execute('''
    SELECT
        d.distrito AS Distrito,
        t.oferta AS Curso
    FROM Alunos a
    JOIN Turmas t ON a.turma = t.cod
    JOIN Escolas e ON t.escola = e.cod
    JOIN Concelhos c ON e.concelho = c.cod
    JOIN Distritos d ON c.distrito = d.cod

    LEFT JOIN EntidadesEscola ee ON t.entidadeEscola = ee.cod
    LEFT JOIN Concelhos cee ON ee.concelho = cee.cod
    LEFT JOIN Distritos dee ON cee.distrito = dee.cod
    WHERE(
        d.distrito IN ("Porto", "Lisboa")
        OR dee.distrito IN ("Porto", "Lisboa")
    )
        AND t.oferta IS NOT NULL
    GROUP BY d.distrito, t.oferta
    ORDER BY d.distrito ASC, t.oferta ASC;
    ''').fetchall()
    return render_template('pergunta2.html', resposta=resposta)

@APP.route('/pergunta/3')
def pergunta3():
    resposta = db.execute('''SELECT
 escolas.escola AS NomeEscola
FROM
    escolas
JOIN
    agrupamentos ON escolas.cod = agrupamentos.codSede
JOIN
    concelhos ON escolas.concelho = concelhos.cod
JOIN
    NUTS_III ON concelhos.NUTSIII = NUTS_III.cod
JOIN
    NUTS_II ON NUTS_III.NUTII = NUTS_II.cod
WHERE
    NUTS_II.NUTII NOT IN ('Centro', 'Alentejo');''').fetchall()
    return render_template('pergunta3.html', resposta=resposta)

@APP.route('/pergunta/4')
def pergunta4():
    resposta = db.execute('''
    SELECT
        sub.distrito AS Distrito,
        MIN(sub.num) AS num
    FROM (
        SELECT
            d.distrito AS distrito,
            COUNT(t.cod) AS num
        FROM distritos d
        JOIN concelhos c ON c.distrito = d.cod
        JOIN escolas e ON e.concelho = c.cod
        JOIN turmas t ON t.escola = e.cod
        WHERE t.nivel LIKE "Ensino Secundário"
        GROUP BY d.cod, d.distrito
    ) AS sub;
    ''').fetchall()
    return render_template('pergunta4.html', resposta=resposta)
  
@APP.route('/pergunta/5')
def pergunta5():
    resposta = db.execute('''
    SELECT
        c.concelho,
        e.escola,
        COUNT(t.cod) AS num
    FROM Turmas t
    JOIN Escolas e ON t.escola = e.cod
    JOIN Concelhos c ON e.concelho = c.cod
    WHERE t.organizacao LIKE '%S3%'
    GROUP BY
        c.concelho,
        e.escola
    ORDER BY
        num DESC,
        c.concelho ASC;
    ''').fetchall()
    return render_template('pergunta5.html', resposta=resposta)


# DIOGO
@APP.route('/explicacao/Subquery_Variavel')
def subqueryVariavel():
    return render_template('explicacaoSubqueryVariavel.html')



@APP.route('/pergunta/6')
def pergunta6():
    resposta = db.execute('''
SELECT
concelhos.concelho as concelho,
agrupamentos.agrupamento as agrupamento
FROM agrupamentos
JOIN escolas ON escolas.agrupamento = agrupamentos.cod
JOIN concelhos ON concelhos.cod = escolas.concelho
JOIN turmas ON turmas.escola = escolas.cod
WHERE turmas.natureza = 'Público' AND turmas.tipologia = 'EB'
GROUP BY concelhos.concelho, agrupamentos.agrupamento
HAVING COUNT(escolas.cod) > 4
ORDER BY
concelhos.concelho,
agrupamentos.agrupamento''').fetchall()
    return render_template('pergunta6.html', resposta=resposta)

@APP.route('/pergunta/7')
def pergunta7():
    resposta = db.execute('''
    WITH MediaRaparigasPorDistrito AS (
        SELECT
            d.distrito,
            AVG(a.quantidade) AS media_raparigas
        FROM distritos d
        JOIN concelhos c ON d.cod = c.distrito
        JOIN escolas e ON c.cod = e.concelho
        JOIN turmas t ON e.cod = t.escola
        JOIN alunos a ON t.cod = a.turma
        WHERE a.sexo = 'Mulheres'
        GROUP BY d.distrito
    ),
    DistritosOrdenados AS (
        SELECT
            distrito,
            media_raparigas,
            ROW_NUMBER() OVER (ORDER BY media_raparigas ASC) AS rank
        FROM MediaRaparigasPorDistrito
    )

    SELECT
        distrito AS Distrito,
        media_raparigas AS med
    FROM DistritosOrdenados
    WHERE rank <= 5
    ORDER BY rank;
    ''').fetchall()
    return render_template('pergunta7.html', resposta=resposta)

@APP.route('/pergunta/8')
def pergunta8():
    resposta = db.execute('''WITH c1 AS (
    SELECT
        distritos.distrito,
        SUM(alunos.quantidade) AS max_quantidade,
        escolas.escola
    FROM distritos
    JOIN concelhos ON concelhos.distrito = distritos.cod
    JOIN escolas ON escolas.concelho = concelhos.cod
    JOIN turmas ON turmas.escola = escolas.cod
    JOIN alunos ON alunos.turma = turmas.cod
    GROUP BY escolas.escola
    HAVING distritos.cod IN (
        SELECT d.cod
        FROM distritos d
        WHERE(
            SELECT COUNT(*)
            FROM concelhos c
            JOIN escolas e ON e.concelho = c.cod
            WHERE c.distrito = d.cod) > 1000)
)

SELECT
    c1.distrito,
    c1.escola,
    MAX(c1.max_quantidade) AS alunos
FROM c1''' ).fetchall()
    return render_template('pergunta8.html', resposta=resposta)
    
@APP.route('/pergunta/9')
def pergunta9():
    resposta = db.execute('''
                          WITH EstatisticasEscolas AS (
    SELECT
        escolas.escola AS NomeEscola,
        COUNT(DISTINCT turmas.cod) AS NumeroTurmas,
        SUM(alunos.quantidade) AS NumeroAlunos
    FROM alunos
    JOIN turmas ON turmas.cod = alunos.turma
    JOIN escolas ON escolas.cod = turmas.escola
    GROUP BY escolas.escola
),


MediasGlobais AS (
    SELECT
        AVG(NumeroTurmas) AS MediaTurmasPorEscola,
        AVG(NumeroAlunos) AS MediaAlunosPorEscola
    FROM EstatisticasEscolas
)


SELECT
    ee.NomeEscola,
    ee.NumeroAlunos,
    CASE
        WHEN ee.NumeroTurmas < mg.MediaTurmasPorEscola THEN 'Tem poucas turmas'
        WHEN ee.NumeroTurmas >= mg.MediaTurmasPorEscola AND ee.NumeroAlunos < mg.MediaAlunosPorEscola THEN 'Poucos alunos'
        WHEN ee.NumeroTurmas >= mg.MediaTurmasPorEscola AND ee.NumeroAlunos >= mg.MediaAlunosPorEscola THEN 'A escola esta sobrepopulada'
    END AS Classificacao
FROM
    EstatisticasEscolas ee
CROSS JOIN
    MediasGlobais mg
ORDER BY
    ee.NomeEscola;''').fetchall()
    return render_template('pergunta9.html', resposta=resposta)

@APP.route('/pergunta/10')
def pergunta10():
    resposta = db.execute('''  
WITH ConcelhosComMaisDeUmNUTSII AS(
WITH NUTSII_Por_Distrito AS (
 SELECT
        d.cod AS DistritoCod,
        CASE
            WHEN COUNT(DISTINCT NUTS_II.NUTII) > 1 THEN TRUE
            ELSE FALSE
        END AS MaisDeUmNUTSII
    FROM
        Distritos d
    JOIN
        Concelhos c ON c.distrito = d.cod
    JOIN
        NUTS_III ON NUTS_III.cod = c.NUTSIII
    JOIN
        NUTS_II ON NUTS_II.cod = NUTS_III.NUTII
    GROUP BY
        d.cod
)
SELECT
    d.distrito,
    c.concelho as concelho,
    c.cod as concelhoCod,
    n.MaisDeUmNUTSII AS MaisDeUmNUTSII
FROM
    Concelhos c
JOIN
    Distritos d ON c.distrito = d.cod
JOIN
    NUTSII_Por_Distrito n ON n.DistritoCod = d.cod
ORDER BY
    d.distrito, c.concelho),

AlunosPorConcelho AS (
    SELECT
        c.Concelho as NomeConcelho,
        SUM(CASE WHEN a.sexo like 'Homens' and ((c.MaisDeUmNUTSII = TRUE AND t.nivel  like 'Ensino básico')
        OR c.MaisDeUmNUTSII = FALSE)
        THEN a.quantidade ELSE 0 END) AS SomaHomensComCondicao,
        SUM(CASE WHEN a.sexo like 'Mulheres' and ((c.MaisDeUmNUTSII = TRUE AND t.nivel like 'Ensino básico') OR c.MaisDeUmNUTSII = FALSE)
        THEN a.quantidade ELSE 0 END) AS SomaMulheresComCondicao,
        SUM(CASE WHEN a.sexo like 'Homens' THEN a.quantidade ELSE 0 END) AS SomaHomensSemCondicao,
        SUM(CASE WHEN a.sexo like 'Mulheres' THEN a.quantidade ELSE 0 END) AS SomaMulheresSemCondicao
    FROM
        ConcelhosComMaisDeUmNUTSII c
    JOIN Escolas e ON e.concelho = c.ConcelhoCod
    JOIN Agrupamentos ag ON ag.codSede = e.cod
    JOIN Turmas t ON t.escola = e.cod
    JOIN Alunos a ON a.turma = t.cod
    GROUP BY
        c.Concelho
)

SELECT
    NomeConcelho,
    SomaHomensComCondicao,
    SomaHomensSemCondicao,
    SomaMulheresComCondicao,
    SomaMulheresSemCondicao,
    c.MaisDeUmNUTSII
FROM
    AlunosPorConcelho
JOIN ConcelhosComMaisDeUmNUTSII c  on c.concelho=AlunosPorConcelho.NomeConcelho
ORDER BY
    NomeConcelho;''').fetchall()
    return render_template('pergunta10.html', resposta=resposta)                      


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
