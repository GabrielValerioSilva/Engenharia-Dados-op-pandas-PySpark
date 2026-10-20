import pandas as pd
import datetime
# Criando e Explorando com Datas e Índices



# 1. Lendo os arquivos gerados
df_alunos = pd.read_csv('alunos.csv')

# 2. Trabalhando com Datas (Datetime)
# Transformando a string de data em um objeto datetime real do Pandas
df_alunos['data_ingresso'] = pd.to_datetime(df_alunos['data_ingresso'])

# 3. Alterando o Índice (Usando set_index)
# Em vez de linhas 0, 1, 2, vamos usar a data de ingresso como o índice da tabela
df_alunos.set_index('data_ingresso', inplace=True) 
# (O inplace=True significa que ele altera o df original, sem precisar criar um "df_novo = ...")

# 4. Buscas baseadas no índice (Saber quem entrou depois de uma certa data)
# "Me mostre todos os alunos que ingressaram depois de Março de 2024"
alunos_recentes = df_alunos[df_alunos.index > pd.to_datetime("2024-03-01")]

# 5. Usando loc e iloc
# .iloc busca pela POSIÇÃO (linha 0, coluna 2)
primeiro_aluno_nome = df_alunos.iloc[0, 1] 

# .loc busca pelo RÓTULO do índice. 
# Se você tivesse feito df_alunos.set_index('matricula', inplace=True), você poderia fazer:
# aluno_especifico = df_alunos.loc[1001]

#Filtragem
df_notas = pd.read_csv('notas.csv')

# 1. Filtro Múltiplo (O '&' funciona como o 'AND' no SQL)
# "Quero ver os alunos que tiraram nota maior que 7.0 E tiveram mais de 75% de presença"
aprovados_com_louvor = df_notas[(df_notas['nota_final'] >= 7.0) & (df_notas['presenca_pct'] > 75)]

# 2. Deletando uma coluna que não importa para a análise (usando axis=1 para indicar que é coluna)
df_notas.drop('id_registro', axis=1, inplace=True)

# 3. Lidando com dados faltantes (Se existissem notas vazias 'NaN')
# df_notas.dropna(axis=0) # Apagaria a LINHA inteira se faltasse a nota
# df_notas['nota_final'].fillna(value=df_notas['nota_final'].mean()) # Preencheria o vazio com a média da turma

#Agrupamentos (Analytics - Descobrindo padrões)
# Lendo dados necessários
df_notas = pd.read_csv('notas.csv')

# "Qual a média de notas e presenças agrupada por cada disciplina?"
media_por_disciplina = df_notas.groupby("id_disciplina").mean(numeric_only=True)

# "Qual foi a menor e a maior nota dada em cada disciplina?"
nota_minima = df_notas.groupby("id_disciplina").min()['nota_final']
nota_maxima = df_notas.groupby("id_disciplina").max()['nota_final']

#Cruzando Tabelas (O "JOIN" do Pandas)
# Carregando as três tabelas que precisamos cruzar
df_notas = pd.read_csv('notas.csv')
df_disciplinas = pd.read_csv('disciplinas.csv')
df_professores = pd.read_csv('professores.csv')

# PASSO 1: Juntar as Notas com as Disciplinas (usando o id_disciplina)
notas_com_disciplinas = pd.merge(df_notas, df_disciplinas, on='id_disciplina')

# PASSO 2: Juntar o resultado acima com os Professores (usando o id_professor)
tabela_geral = pd.merge(notas_com_disciplinas, df_professores, on='id_professor')

# O GRANDE FINAL (Analytics Engineering):
# "Me mostre a nota média, separada por Tipo de Professor (Ministrante ou Adjunto) e Nome do Professor"
analise_professores = tabela_geral.groupby(['tipo_professor', 'nome_professor'])['nota_final'].mean().reset_index()

# Ordenando do professor que dá a nota mais alta para o mais carrasco
analise_professores = analise_professores.sort_values(by='nota_final', ascending=False)
print(analise_professores)


