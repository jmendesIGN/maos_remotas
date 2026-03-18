# ============================================================
# CONFIGURAÇÕES DA AUTOMAÇÃO SKYNET x QUICKBASE
# Preencha os campos abaixo antes de executar o script
# ============================================================

# --- OPENAI ---
# Sua chave de API da OpenAI
# Acesse: platform.openai.com > API Keys
OPENAI_API_KEY = "SUA_CHAVE_OPENAI_AQUI"

# Modelo a ser usado
OPENAI_MODEL = "gpt-4.1"

# --- QUICKBASE ---
# Realm: parte do endereço do seu Quickbase
# Ex: se o endereço é "empresa.quickbase.com", o realm é "empresa"
QUICKBASE_REALM = "SEU_REALM_AQUI"

# Token de acesso ao Quickbase
# Acesse: Quickbase > Configurações > Tokens de usuário
QUICKBASE_USER_TOKEN = "SEU_TOKEN_AQUI"

# ID da tabela de serviços no Quickbase
# Ex: "bpqxxxxx" — aparece na URL quando você abre a tabela
QUICKBASE_TABLE_ID = "SEU_TABLE_ID_AQUI"

# --- IDs DOS CAMPOS NA TABELA DO QUICKBASE ---
# Para encontrar o ID de um campo: abra a tabela > Configurações > Campos
# Cada campo tem um número (ex: Field ID = 7)
FIELD_ID_PID = 0           # ID do campo onde ficam os números PID
FIELD_ID_TT = 0            # ID do campo onde ficam os números TT
FIELD_ID_ACC = 0           # ID do campo onde ficam os códigos ACC (Starlink)
FIELD_ID_TECH_ACTIVITY = 0 # ID do campo onde ficam os números Tech Activity
FIELD_ID_SID = 0           # ID do campo SID (valor que queremos buscar)
FIELD_ID_STATUS = 0        # ID do campo Status (para atualizar para "Pago")

# --- ARQUIVO DA PLANILHA ---
# Caminho completo do arquivo a ser processado
# Pode ser .xlsx ou .csv
ARQUIVO_PLANILHA = r"C:\Users\Jeimili Mendes\Documents\projetos\modelo.xlsx"
