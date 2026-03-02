# Agente de Atendimento

API FastAPI para atendimento automatizado.

## Pré-requisitos

- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)
- Virtual environment recomendado

## Instalação

### 1. Criar ambiente virtual

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

### 2. Instalar dependências

```bash
pip install -e ".[dev]"
```

### 3. Configurar variáveis de ambiente

```bash
cp .env.example .env
# Edite o arquivo .env conforme necessário
```

## Executar o Projeto

### Modo desenvolvimento

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Acesse: http://localhost:8000

### API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Executar Testes

```bash
# Rodar todos os testes
pytest

# Rodar com cobertura
pytest --cov=src --cov-report=html

# Rodar com verbosidade
pytest -v
```

## Lint e Type Check

```bash
# Formatar código
black src/ tests/

# Verificar lint
ruff check src/ tests/

# Type checking
mypy src/
```

## Estrutura do Projeto

```
repo/
├── .gitignore          # Arquivos ignorados pelo Git
├── .env.example        # Exemplo de variáveis de ambiente
├── README.md           # Documentação do projeto
├── pyproject.toml      # Dependências e configuração Python
├── src/
│   ├── __init__.py
│   ├── main.py         # Entry point da aplicação FastAPI
│   ├── config.py       # Configurações (env, logging)
│   └── api/
│       ├── __init__.py
│       └── routes/
└── tests/
    ├── __init__.py
    ├── conftest.py     # Configuração pytest
    └── test_main.py
```

## Licença

MIT
