from airflow.providers.http.operators.http import HttpOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow import DAG
from datetime import datetime
import json

def gerar_relatorio_matriculas(**kwargs):
    ti = kwargs['ti']
    resposta_api = ti.xcom_pull(task_ids='obter_dados_api_academica', key="return_value")
    
    alunos = json.loads(resposta_api) 

    # Adaptando a lógica original para analisar o status de matrículas da Universidade
    matriculas_ativas = len([aluno for aluno in alunos if aluno.get('matricula_ativa')])
    matriculas_inativas = len([aluno for aluno in alunos if not aluno.get('matricula_ativa')])

    total_alunos = len(alunos)
    porcentagem_ativas = (matriculas_ativas / total_alunos) * 100 if total_alunos > 0 else 0
    porcentagem_inativas = (matriculas_inativas / total_alunos) * 100 if total_alunos > 0 else 0

    print(f'Porcentagem de matrículas ativas: {porcentagem_ativas:.2f}%')
    print(f'Porcentagem de matrículas inativas (evasão/trancamento): {porcentagem_inativas:.2f}%')

# Definindo o DAG com o contexto 'with'
with DAG(
    dag_id='exemplo_http_operator_universidade',
    description='DAG com HttpOperator e PythonOperator para relatório de alunos',
    start_date=datetime(2025, 10, 22),
    catchup=False,
) as dag:

    obter_dados_api = HttpOperator(
        task_id='obter_dados_api_academica',
        http_conn_id="api_sistema_universidade",
        endpoint="alunos", # Endpoint genérico da instituição
        method="GET",
        headers={"Content-Type": "application/json"},
        response_filter=lambda response: response.text,
        log_response=True,
    )

    gerar_relatorio_task = PythonOperator(
        task_id="gerar_relatorio_matriculas",
        python_callable=gerar_relatorio_matriculas
    )

    obter_dados_api >> gerar_relatorio_task