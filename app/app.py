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

     -- Relacionar com EntidadesEscola
    LEFT JOIN EntidadesEscola ee ON t.entidadeEscola = ee.cod
    LEFT JOIN Concelhos cee ON ee.concelho = cee.cod
    LEFT JOIN Distritos dee ON cee.distrito = dee.cod
    WHERE(
        d.distrito IN ('Porto', 'Lisboa')
        OR dee.distrito IN ('Porto', 'Lisboa')
    )
        AND t.oferta NOT NULL
    GROUP BY d.distrito, t.oferta
    ORDER BY d.distrito ASC, t.oferta ASC;
    ''').fetchall()
    return render_template('pergunta2.html')

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
    return render_template('pergunta4.html')

@APP.route('/pergunta/5')
def pergunta5():
    return render_template('pergunta5.html')

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
    return render_template('pergunta7.html')

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