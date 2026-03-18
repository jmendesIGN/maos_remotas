"""
Agente GPT-4.1 — Automação Skynet x Quickbase
----------------------------------------------
Usa function calling da OpenAI para orquestrar a conferência
da planilha: busca no Quickbase, atualiza SID e status.
"""

import json
import logging
from datetime import datetime
from pathlib import Path

from openai import OpenAI

import config
import tools

log = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent

SYSTEM_PROMPT = """
Você é um agente de automação contábil. Sua tarefa é processar todas as linhas
de uma planilha do provedor Skynet e, para cada linha:

1. Identificar o tipo e valor do identificador na coluna "IGN Network":
   - PID#####          → tipo=PID, valor=apenas os dígitos (ex: PID15241 → valor="15241")
   - TT######          → tipo=TT, valor=apenas os dígitos (ex: TT293815 → valor="293815")
   - ACC-...           → tipo=ACC, valor=código completo (ex: "ACC-4242771-34437-13")
   - Tech Activity#### → tipo=TECH_ACTIVITY, valor=apenas os dígitos

2. Chamar buscar_no_quickbase(tipo, valor) para obter o SID.

3. Chamar atualizar_sid_planilha com:
   - numero_linha: o campo _numero_linha da linha
   - sid: o SID retornado (ou "NULL" se não encontrado)
   - encontrado: True se foi encontrado, False se não
   - especial: True apenas se o SID retornado for igual ao próprio identificador (PID=SID)

4. Se o serviço foi encontrado (encontrado=True), chamar atualizar_status_quickbase.

5. Ao finalizar TODAS as linhas, chamar salvar_planilha().

6. Por fim, me retorne um relatório em texto com:
   - Total de linhas processadas
   - Quantidade com SID encontrado
   - Quantidade NULL (não encontrados) — liste o responsável de cada um
   - Quantidade de casos especiais

Processe uma linha de cada vez. Não pule linhas.
Se uma linha não tiver identificador reconhecível, registre como sem identificador e continue.
""".strip()


def rodar_agente(linhas: list[dict]) -> str:
    """
    Executa o agente GPT-4.1 sobre as linhas da planilha.
    Retorna o relatório final gerado pelo agente.
    """
    client = OpenAI(api_key=config.OPENAI_API_KEY)

    # Monta a mensagem inicial com os dados da planilha
    dados_planilha = json.dumps(linhas, ensure_ascii=False, indent=2)
    mensagem_usuario = f"Processe as seguintes {len(linhas)} linhas da planilha Skynet:\n\n{dados_planilha}"

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": mensagem_usuario},
    ]

    log.info(f"Agente iniciado — {len(linhas)} linhas para processar")
    iteracao = 0

    while True:
        iteracao += 1
        log.info(f"Iteração {iteracao}: enviando para GPT-4.1...")

        response = client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=messages,
            tools=tools.TOOLS_SCHEMA,
            tool_choice="auto",
            timeout=120,
        )

        choice = response.choices[0]
        messages.append(choice.message)

        # Agente terminou — sem mais tool calls
        if choice.finish_reason == "stop":
            relatorio = choice.message.content or ""
            log.info("Agente concluído.")
            return relatorio

        # Agente quer chamar ferramentas
        if choice.finish_reason == "tool_calls" and choice.message.tool_calls:
            for tool_call in choice.message.tool_calls:
                nome = tool_call.function.name
                argumentos = tool_call.function.arguments
                log.info(f"  Tool: {nome}({argumentos[:80]}...)" if len(argumentos) > 80 else f"  Tool: {nome}({argumentos})")

                resultado = tools.executar_ferramenta(nome, argumentos)

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": resultado,
                })

        # Segurança: evita loop infinito
        if iteracao > 2000:
            log.warning("Número máximo de iterações atingido.")
            break

    return "Execução encerrada."


def salvar_relatorio(relatorio: str) -> None:
    """Salva o relatório textual gerado pelo agente."""
    nome = BASE_DIR / f"relatorio_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    with open(nome, "w", encoding="utf-8") as f:
        f.write(relatorio)
    log.info(f"Relatório salvo: {nome}")
