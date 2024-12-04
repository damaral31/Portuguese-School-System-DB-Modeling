import pandas as pd 
import sqlite3

# Ler o ficheiro Excel
df = pd.read_excel('AlunosMatriculados17.xlsx')

# Conectar à base de dados
conn = sqlite3.connect('AlunosMatriculados.db')
cursor = conn.cursor()

'''# Apagar todos os dados das colunas cod e NUTII
cursor.execute("DELETE FROM NUTSII")

# Extrair a coluna 'NUTS II (2013)' do DataFrame e convertê-la numa lista
NUTSII = df['NUTS II (2013)'].unique().tolist()

# Inserir os novos dados na tabela NUTSII
j = 1
for i in NUTSII:
    cursor.execute("INSERT INTO NUTSII (cod, NUTII) VALUES (?, ?)", (j, i))
    j += 1

# Confirmar as alterações na base de dados
conn.commit()

# Extrair as colunas 'NUTS III (2013)' e 'NUTS II (2013)' do DataFrame e convertê-las numa lista de tuplas
NUTSIII = df[['NUTS III (2013)', 'NUTS II (2013)']].drop_duplicates().values.tolist()

# Apagar todos os dados da tabela NUTSIII
cursor.execute("DELETE FROM NUTSIII")

# Inserir os novos dados na tabela NUTSIII
cod = 10
for nutsiii, nutsii in NUTSIII:
    cursor.execute("SELECT cod FROM NUTSII WHERE NUTII = ?", (nutsii,))
    nutsii_cod = cursor.fetchone()[0]
    cursor.execute("INSERT INTO NUTSIII (cod, NUTIII, NUTSII) VALUES (?, ?, ?)", (cod, nutsiii, nutsii_cod))
    cod += 1

# Confirmar as alterações na base de dados
'''

Distritos = df['DISTRITO'].unique().tolist()
cod_distrito = 50
for distrito in Distritos:
    cursor.execute("INSERT INTO DISTRITOS (cod, distrito) VALUES (?, ?)", (cod_distrito, distrito))
    cod_distrito += 1


conn.commit()
conn.close()