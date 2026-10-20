from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

# Definindo o DAG
dag = DAG(
    dag_id='exemplo_bash_operator_universidade',
    description='DAG simples com BashOperator manipulando arquivos acadêmicos',
    start_date=datetime(2025, 10, 22),
    catchup=False,
)

# Etapa 1: Criando um diretório para relatórios da coordenação
criar_diretorio = BashOperator(
    task_id='criar_diretorio_coordenacao',
    bash_command='mkdir -p /tmp/universidade_relatorios',
    dag=dag,
)

# Etapa 2: Salvando lista de arquivos no diretório temporário
salvar_lista_arquivos = BashOperator(
    task_id='salvar_lista_arquivos_disciplinas',
    bash_command='ls / > /tmp/universidade_relatorios/disciplinas_arquivadas.txt',
    dag=dag,
)

# Etapa 3: Imprimindo a lista de arquivos com echo
imprimir_lista_arquivos = BashOperator(
    task_id='imprimir_lista_arquivos',
    bash_command='cat /tmp/universidade_relatorios/disciplinas_arquivadas.txt | xargs echo',
    dag=dag,
)

criar_diretorio >> salvar_lista_arquivos >> imprimir_lista_arquivos