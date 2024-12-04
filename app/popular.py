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
'''
turmas = df[['CÓDIGO DGEEC ESCOLA', 'CÓDICO DGEEC ENTIDADE', 'NATUREZA', 'ORIENTAÇÃO', 'NÍVEL DE  ENSINO', 'OFERTA', 'TIPOLOGIA', 'ANO DE ESCOLARIDADE', 'CICLO DE ESTUDOS', 'ORGANIZAÇÃO','CURSO']].drop_duplicates().values.tolist()
cursor.execute("DELETE FROM TURMAS")
cod_turma = 1000
for codigo_escola, codigo_entidade, natureza, orientacao, nivel, oferta, tipologia, ano, ciclo, organizacao,curso in turmas:
    if pd.notnull(codigo_escola):
        cursor.execute("INSERT INTO TURMAS (cod, escola, entidadeEscola, natureza, orientacao, nivel, oferta, tipologia, ano, ciclo, organizacao) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       (cod_turma, codigo_escola, None, natureza, orientacao, nivel, oferta, tipologia, ano, ciclo, organizacao,curso))
    else:
        cursor.execute("INSERT INTO TURMAS (cod, escola, entidadeEscola, natureza, orientacao, nivel, oferta, tipologia, ano, ciclo, organizacao) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       (cod_turma, None, codigo_entidade, natureza, orientacao, nivel, oferta, tipologia, ano, ciclo, organizacao,curso))
        cod_turma += 1


conn.commit()
conn.close()