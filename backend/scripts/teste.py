#!/usr/bin/env python
from dotenv import load_dotenv
load_dotenv()

import os, sys

from backend.src.collect.tasks.contratacoes import coletar_contratacoes

if __name__ == "__main__":
    # Data para teste no formato YYYYMMDD
    data_inicial = "20250101"
    data_final = "20250101"
    
    print(f"Iniciando coleta de contratações de {data_inicial} até {data_final}")
    
    # Executa a task de forma assíncrona via Celery
    resultado = coletar_contratacoes.delay(data_inicial, data_final)
    
    # Mostra o ID da task
    print(f"Task iniciada com ID: {resultado.id}")
    
    # Aguarda o resultado (timeout de 5 minutos)
    print("Aguardando resultado...")
    resultado_final = resultado.get(timeout=300)
    
    print(f"Resultado da task: {resultado_final}")
