import pandas as pd 
import sqlite3

# Ler o ficheiro Excel
df = pd.read_excel('AlunosMatriculados17.xlsx')

# Conectar à base de dados
conn = sqlite3.connect('AlunosMatriculados.db')
cursor = conn.cursor()

'''# Apagar todos os dados das colunas cod e NUTII
cursor.execute("DELETE FROM NUTS_II")

# Extrair a coluna 'NUTS II (2013)' do DataFrame e convertê-la numa lista
NUTSII = df['NUTS II (2013)'].unique().tolist()

# Inserir os novos dados na tabela NUTSII
j = 1
for i in NUTSII:
    cursor.execute("INSERT INTO NUTS_II (cod, NUTII) VALUES (?, ?)", (j, i))
    j += 1

# Confirmar as alterações na base de dados
conn.commit()

# Extrair as colunas 'NUTS III (2013)' e 'NUTS II (2013)' do DataFrame e convertê-las numa lista de tuplas
NUTSIII = df[['NUTS III (2013)', 'NUTS II (2013)']].drop_duplicates().values.tolist()

# Apagar todos os dados da tabela NUTSIII
cursor.execute("DELETE FROM NUTS_III")

# Inserir os novos dados na tabela NUTSIII
cod = 10
for nutsiii, nutsii in NUTSIII:
    cursor.execute("SELECT cod FROM NUTS_II WHERE NUTII = ?", (nutsii,))
    nutsii_cod = cursor.fetchone()[0]
    cursor.execute("INSERT INTO NUTS_III (cod, NUTIII, NUTII) VALUES (?, ?, ?)", (cod, nutsiii, nutsii_cod))
    cod += 1

# Confirmar as alterações na base de dados


Distritos = df['DISTRITO'].unique().tolist()
cod_distrito = 50
for distrito in Distritos:
    cursor.execute("INSERT INTO DISTRITOS (cod, distrito) VALUES (?, ?)", (cod_distrito, distrito))
    cod_distrito += 1



concelhos = df[['CONCELHO', 'DISTRITO', 'NUTS III (2013)']].drop_duplicates().values.tolist()
#cursor.execute("DELETE FROM CONCELHOS")
cod_concelho = 100
for concelho, distrito, nutsiii in concelhos:
    cursor.execute("SELECT cod FROM DISTRITOS WHERE distrito = ?", (distrito,))
    distrito_cod = cursor.fetchone()[0]
    cursor.execute("SELECT cod FROM NUTS_III WHERE NUTIII = ?", (nutsiii,))
    nutsiii_cod = cursor.fetchone()[0]
    cursor.execute("INSERT INTO CONCELHOS (cod, concelho, NUTSIII, distrito) VALUES (?, ?, ?, ?)", (cod_concelho, concelho, nutsiii_cod, distrito_cod))
    cod_concelho += 1

esntidades = df[df['AGRUPAMENTO'].notnull()][['CÓDIGO DGEEC AGRUPAMENTO', 'CÓDIGO DGEEC ESCOLA SEDE', 'AGRUPAMENTO']].drop_duplicates().values.tolist()
cursor.execute("DELETE FROM ENTIDADES")
for entidade in esntidades:
    cursor.execute("INSERT INTO Agrupamentos (cod, codSede, agrupamento) VALUES (?, ?, ?)", (entidade[0], entidade[1], entidade[2]))
  

escola = df[df['CÓDIGO DGEEC ESCOLA'].notnull() & df['ESCOLA'].notnull()][['CÓDIGO DGEEC ESCOLA', 'CÓDICO DGEEC ENTIDADE', 'ESCOLA', 'CÓDIGO DGEEC AGRUPAMENTO', 'CONCELHO']].drop_duplicates().values.tolist()
cursor.execute("DELETE FROM ESCOLA")
for codigo_escola, codigo_entidade, escola, codigo_agrupamento, concelho in escola:
    cursor.execute("SELECT cod FROM concelhos WHERE concelho = ?", (concelho,))
    concelho_cod = cursor.fetchone()[0]
    cursor.execute("INSERT INTO ESCOLA (cod, entidade, escola, agrupamento, concelho) VALUES (?, ?, ?, ?, ?)", (codigo_escola, codigo_entidade, escola, codigo_agrupamento, concelho_cod))
  
entidades = df[['CÓDICO DGEEC ENTIDADE', 'ENTIDADE']].drop_duplicates().values.tolist()
cursor.execute("DELETE FROM ENTIDADES")
for entidade in entidades:
    cursor.execute("INSERT INTO ENTIDADES (cod, entidade) VALUES (?, ?)", (entidade[0], entidade[1]))

turmas = df[['CÓDIGO DGEEC ESCOLA', 'CÓDICO DGEEC ENTIDADE', 'NATUREZA', 'ORIENTAÇÃO', 'NÍVEL DE  ENSINO', 'OFERTA', 'TIPOLOGIA', 'ANO DE ESCOLARIDADE', 'CICLO DE ESTUDOS', 'ORGANIZAÇÃO','CURSO']].drop_duplicates().values.tolist()
cursor.execute("DELETE FROM TURMAS")
cod_turma = 1000
for codigo_escola, codigo_entidade, natureza, orientacao, nivel, oferta, tipologia, ano, ciclo, organizacao,curso in turmas:
    cursor.execute("INSERT INTO TURMAS (cod, escola, entidadeEscola, natureza, orientacao, nivel, oferta, tipologia, ano, ciclo, organizacao,curso) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
    (cod_turma, codigo_escola, codigo_entidade, natureza, orientacao, nivel, oferta, tipologia, ano, ciclo, organizacao,curso))
        
    cod_turma += 1

i = 0
alunos = df[['CÓDIGO DGEEC ESCOLA', 'CÓDICO DGEEC ENTIDADE', 'NATUREZA', 'ORIENTAÇÃO', 'NÍVEL DE  ENSINO', 'OFERTA', 'TIPOLOGIA', 'ANO DE ESCOLARIDADE', 'CICLO DE ESTUDOS', 'ORGANIZAÇÃO', 'CURSO', 'SEXO', 'NÚMERO DE ALUNOS MATRICULADOS']].drop_duplicates().values.tolist()
cursor.execute("DELETE FROM ALUNOS")

for codigo_escola, codigo_entidade, natureza, orientacao, nivel, oferta, tipologia, ano, ciclo, organizacao, curso, sexo, alunos in alunos:
    query = """
    SELECT cod FROM TURMAS WHERE 
    (escola IS NULL OR escola = ?) AND 
    (entidadeEscola IS NULL OR entidadeEscola = ?) AND 
    (natureza IS NULL OR natureza = ?) AND 
    (orientacao IS NULL OR orientacao = ?) AND 
    (nivel IS NULL OR nivel = ?) AND 
    (oferta IS NULL OR oferta = ?) AND 
    (tipologia IS NULL OR tipologia = ?) AND 
    (ano IS NULL OR ano = ?) AND 
    (ciclo IS NULL OR ciclo = ?) AND 
    (organizacao IS NULL OR organizacao = ?) AND 
    (curso IS NULL OR curso = ?)
    """
    cursor.execute(query, (
        None if pd.isnull(codigo_escola) else codigo_escola,
        None if pd.isnull(codigo_entidade) else codigo_entidade,
        None if pd.isnull(natureza) else natureza,
        None if pd.isnull(orientacao) else orientacao,
        None if pd.isnull(nivel) else nivel,
        None if pd.isnull(oferta) else oferta,
        None if pd.isnull(tipologia) else tipologia,
        None if pd.isnull(ano) else ano,
        None if pd.isnull(ciclo) else ciclo,
        None if pd.isnull(organizacao) else organizacao,
        None if pd.isnull(curso) else curso
    ))
    turma_cod = cursor.fetchone()
    if turma_cod:
        turma_cod = turma_cod[0]
        print(turma_cod, i)
        cursor.execute("INSERT INTO ALUNOS (turma, sexo, quantidade) VALUES (?, ?, ?)", (turma_cod, sexo, alunos))
        i += 1

esntidadesescola = df[df['ESCOLA'].isnull()][[ 'CÓDICO DGEEC ENTIDADE', 'ENTIDADE', 'CONCELHO']].drop_duplicates().values.tolist()

for entidade in esntidadesescola:
    cursor.execute("select cod from concelhos where concelho = ?", (entidade[2],))
    concelho_cod = cursor.fetchone()[0]
    cursor.execute("INSERT INTO ENTIDADESescola (cod, entidade, concelho) VALUES (?, ?, ?)", (entidade[0], entidade[1], concelho_cod))
'''
conn.commit()
conn.close()