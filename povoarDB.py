import db
import pandas as pd

file_path = 'DGEEC_AlunosMatriculados_2017_2018.xlsx'
data = pd.read_excel(file_path)
data.dropna(subset=["ANO LETIVO", "CÓDIGO DGEEC ENTIDADE"] inplace=True)
print(data.columns)

def povoarEnatidades():
    for entidade in data["ENTIDADE"].unique():
        
        


