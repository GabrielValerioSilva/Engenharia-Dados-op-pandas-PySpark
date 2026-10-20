from airflow import DAG
from airflow.providers.standard.operators.python import PythonOperator, BranchPythonOperator
from datetime import datetime
import random

# Função de decisão de rotina acadêmica
def decidir_caminho_academico():
    return random.choice(['fluxo_fechamento_semestre', 'fluxo_atualizacao_diaria'])

# Função para tarefas de fim de semestre
def fluxo_fechamento():
    print("Executando fechamento de semestre: calculando médias finais dos alunos.")

# Função para tarefas diárias
def fluxo_diario():
    print("Executando fluxo diário: atualizando presenças e acessos nas catracas.")

# Definindo o DAG com o contexto 'with'
with DAG(
    dag_id='exemplo_branching_universidade',
    description='DAG com BranchPythonOperator para processos acadêmicos',
    start_date=datetime(2025, 10, 22),
    catchup=False,
) as dag:

    # Etapa 1: Decisão de fluxo
    decidir = BranchPythonOperator(
        task_id='decidir_fluxo',
        python_callable=decidir_caminho_academico,
    )

    # Fluxo 1: Fechamento de Semestre
    fluxo_1_task = PythonOperator(
        task_id='fluxo_fechamento_semestre',
        python_callable=fluxo_fechamento,
    )

    # Fluxo 2: Atualização Diária
    fluxo_2_task = PythonOperator(
        task_id='fluxo_atualizacao_diaria',
        python_callable=fluxo_diario,
    )

    # Definindo a ordem de execução
    decidir >> [fluxo_1_task, fluxo_2_task] # type: ignore