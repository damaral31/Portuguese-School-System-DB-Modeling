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