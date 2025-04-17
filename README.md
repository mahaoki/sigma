# 🚀 Projeto Sigma - ETL PNCP

O **Sigma** é um projeto de ETL (Extract, Transform, Load) voltado para coleta, validação, estruturação e análise de dados públicos da API do **PNCP (Portal Nacional de Contratações Públicas)**. Seu objetivo é oferecer uma base robusta e atualizada de informações sobre contratações governamentais, permitindo consultas e insights para fornecedores e agentes do mercado público.

---

## ✨ Principais Funcionalidades

- Coleta de dados da API PNCP (v1)
- Checagem de versões de contratações por período e modalidade
- Gravação de controles de publicação/atualização em banco `raw`
- Task assíncrona com Celery para cada etapa (coleta, validação, ETL)
- Validação de registros novos, atualizados e ignorados
- Mecanismo de orquestração com `chord()` entre subtarefas e callback
- Controle de reprocessamento e tentativas automatizadas

---

## 🧱 Stack Principal

- **Linguagem**: Python 3.11+
- **ETL Engine**: Celery + Redis
- **Banco de dados**: PostgreSQL
- **ORM**: SQLAlchemy
- **Framework Web/API**: FastAPI (em progresso)
- **Gerenciador de tarefas**: Flower (para monitoramento Celery)

---

## 🔄 Fluxo de Execução

1. A orquestração é iniciada via task `check_flow` (por data e modo `reprocessing`)
2. É criado (ou reutilizado) um `ProcessingPeriod`
3. Duas subtarefas são enfileiradas:
    - `check_publication`: coleta dados da publicação
    - `check_update`: coleta dados de atualização
4. Ao final, `validate_procurement_versions` é executada via `chord()`
5. A task de validação classifica cada contratação como:
    - `new`
    - `updated`
    - `ignored`

---

## 📂 Estrutura de Diretórios

```
sigma/
├── backend/
│   ├── db/                # Models e sessões SQLAlchemy
│   ├── engines/          # Engine principal de checking
│   ├── tasks/            # Tasks Celery (checagem, validação, ETL)
│   ├── control/          # Funções auxiliares de controle
│   ├── orchestrators/    # Orquestrador principal Celery
│   ├── helpers/          # Funções de logging, parsing, etc
│   └── config/           # Configurações do projeto
├── scripts/              # Execução manual de rotinas
├── tests/                # Testes unitários com Pytest
└── README.md             # Este arquivo
```

---

## 🚫 Evitação de Problemas

- O `period_id` é passado para todas as tasks para garantir consistência
- O commit do `ProcessingPeriod` é feito **antes** de enfileirar subtarefas (evita invisibilidade transacional)
- `ProcurementCheck` tem constraint única para evitar duplicidade
- `save_procurement_check` usa upsert: atualiza se já existir
- Retry automático desativado em dev via `settings.IS_DEV`

---

## 🚧 Em andamento

- Implementação da coleta detalhada para registros `new`
- ETL de entidades: procurement, items, contratos, documentos etc
- Interface web para acompanhamento dos períodos e logs
- Exportação para camada `dw`

---

## 📆 Exemplo de execução

```bash
python scripts/run_check_flow.py --start-date 2025-01-01 --end-date 2025-01-01 --reprocessing
```

---

## 📚 Licença

Este projeto é de uso interno. Direitos reservados ao autor Mahmoud Aoki. Ainda não licenciado publicamente.
