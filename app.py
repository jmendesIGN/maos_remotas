"""
Automação: Conferência Planilha Skynet x Quickbase
---------------------------------------------------
Ponto de entrada. Carrega a planilha e dispara o agente GPT-4.1.

Como usar:
  1. Preencha config.py com suas credenciais
  2. Execute: python app.py
"""

import logging
from pathlib import Path

import config
import tools
import agent

# ── Configuração do log ────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).parent

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(BASE_DIR / "execucao.log", encoding="utf-8"),
        logging.StreamHandler(),
    ],
)
log = logging.getLogger(__name__)


def main():
    print("=" * 60)
    print("  AUTOMAÇÃO SKYNET x QUICKBASE — Agente GPT-4.1")
    print("=" * 60)
    print(f"  Arquivo: {config.ARQUIVO_PLANILHA}")
    print()

    # Valida configurações mínimas
    if "SUA_CHAVE" in config.OPENAI_API_KEY or not config.OPENAI_API_KEY:
        print("ERRO: Configure OPENAI_API_KEY em config.py antes de executar.")
        return
    if "SEU_REALM" in config.QUICKBASE_REALM or not config.QUICKBASE_REALM:
        print("ERRO: Configure QUICKBASE_REALM em config.py antes de executar.")
        return

    # Carrega a planilha
    log.info("Carregando planilha...")
    linhas = tools.inicializar_planilha(config.ARQUIVO_PLANILHA)

    if not linhas:
        print("ERRO: Nenhuma linha encontrada na planilha.")
        return

    print(f"  {len(linhas)} linhas carregadas. Iniciando agente...\n")

    # Executa o agente
    relatorio = agent.rodar_agente(linhas)

    # Exibe e salva o relatório
    print("\n" + "=" * 60)
    print(relatorio)
    print("=" * 60)
    agent.salvar_relatorio(relatorio)


if __name__ == "__main__":
    main()
