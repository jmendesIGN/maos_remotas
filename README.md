Automação Skynet x Quickbase — Agente GPT-4.1

Agente de automação contábil que lê uma planilha do provedor **Skynet**, busca os registros correspondentes no **Quickbase** e preenche automaticamente a coluna SID com formatação visual por cor.

Como funciona

O agente GPT-4.1 recebe as linhas da planilha e, para cada uma:

1. Identifica o tipo de identificador na coluna **IGN Network**:
   - `PID#####` — número de PID
   - `TT######` — número de TT
   - `ACC-...` — código ACC (ex: Starlink)
   - `Tech Activity####` — número de Tech Activity

2. Consulta o Quickbase via API para buscar o SID correspondente

3. Preenche a coluna SID na planilha com cor indicativa:
   - **Verde** — SID encontrado
   - **Vermelho** — não encontrado (NULL)
   - **Amarelo** — caso especial (PID = SID)

4. Atualiza o status do registro no Quickbase para `"Pago"` quando encontrado

5. Salva a planilha e gera um relatório textual com o resumo da execução

Estrutura do projeto

```
├── app.py          # Ponto de entrada — carrega a planilha e inicia o agente
├── agent.py        # Loop do agente GPT-4.1 com function calling
├── tools.py        # Ferramentas do agente (Quickbase API + manipulação da planilha)
├── config.py       # Configurações e credenciais (editar antes de usar)
└── requirements.txt
```

 Pré-requisitos

- Python 3.11+
- Conta na [OpenAI](https://platform.openai.com) com acesso ao modelo `gpt-4.1`
- Conta no [Quickbase](https://quickbase.com) com token de usuário

 Instalação

```bash
pip install -r requirements.txt
```

 Configuração

Edite o arquivo `config.py` preenchendo suas credenciais:

```python
# OpenAI
OPENAI_API_KEY = "sk-..."
OPENAI_MODEL   = "gpt-4.1"

# Quickbase
QUICKBASE_REALM      = "sua-empresa"   # parte antes de .quickbase.com
QUICKBASE_USER_TOKEN = "..."
QUICKBASE_TABLE_ID   = "bpqxxxxx"

# IDs dos campos na tabela do Quickbase
FIELD_ID_PID           = 0   # campo com números PID
FIELD_ID_TT            = 0   # campo com números TT
FIELD_ID_ACC           = 0   # campo com códigos ACC
FIELD_ID_TECH_ACTIVITY = 0   # campo com números Tech Activity
FIELD_ID_SID           = 0   # campo SID (valor buscado)
FIELD_ID_STATUS        = 0   # campo Status (atualizado para "Pago")

# Planilha a processar (.xlsx ou .csv)
ARQUIVO_PLANILHA = r"C:\caminho\para\planilha.xlsx"
```

> **Como encontrar o ID de um campo no Quickbase:** abra a tabela → Configurações → Campos. Cada campo exibe seu número (Field ID).

 Uso

```bash
python app.py
```

O script irá:
- Carregar e exibir a quantidade de linhas da planilha
- Processar cada linha via agente GPT-4.1
- Salvar a planilha atualizada com as cores
- Gerar um arquivo `relatorio_YYYYMMDD_HHMM.txt` com o resumo
- Gravar log detalhado em `execucao.log`


 Dependências

| Pacote     | Versão      | Uso                              |
|------------|-------------|----------------------------------|
| openai     | ≥ 1.30.0    | Agente GPT-4.1 com function calling |
| openpyxl   | 3.1.5       | Leitura e escrita de planilhas   |
| requests   | 2.32.3      | Chamadas à API do Quickbase      |
