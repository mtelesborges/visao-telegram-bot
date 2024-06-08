from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from configs.const import (
    BOTAO_CANCELAR,
    BOTAO_CODIGO,
    BOTAO_FINALIZAR,
    BOTAO_FOTO,
    CHOOSING,
    TYPING_CHOICE,
    TYPING_REPLY,
)
from configs.logger import logger
from handlers.cancelar_marcacao_ponto_handler import (
    cancelar_marcacao_ponto_handler,
)
from handlers.compartilhando_localizacao_handler import (
    compartilhando_localizacao,
)
from handlers.escolhendo_opcao_marcacao_ponto_handler import (
    escolhendo_opcao_marcacao_ponto,
)
from handlers.finalizar_marcacao_ponto_handler import finalizar_marcacao_ponto
from handlers.iniciar_marcacao_ponto_handler import (
    iniciar_marcacao_ponto_handler,
)
from handlers.salvar_dado_informado_handler import (
    salvar_dado_informado_handler,
)


informar_dados_ponto_handler = ConversationHandler(
    entry_points=[iniciar_marcacao_ponto_handler],
    states={
        CHOOSING: [
            cancelar_marcacao_ponto_handler,
            MessageHandler(
                filters.Regex(f"^({BOTAO_CODIGO}|{BOTAO_FOTO})$"),
                escolhendo_opcao_marcacao_ponto,
            ),
            MessageHandler(
                filters.Regex(f"^({BOTAO_FINALIZAR})$"),
                finalizar_marcacao_ponto,
            ),
            MessageHandler(
                filters.ALL & ~filters.COMMAND, compartilhando_localizacao
            ),
        ],
        TYPING_CHOICE: [
            MessageHandler(
                filters.TEXT
                & ~(filters.COMMAND | filters.Regex(f"^{BOTAO_CANCELAR}$")),
                escolhendo_opcao_marcacao_ponto,
            )
        ],
        TYPING_REPLY: [
            MessageHandler(
                filters.Regex(f"^({BOTAO_FINALIZAR})$"),
                finalizar_marcacao_ponto,
            ),
            MessageHandler(
                filters.Regex(f"^({BOTAO_CODIGO}|{BOTAO_FOTO})$"),
                escolhendo_opcao_marcacao_ponto,
            ),
            salvar_dado_informado_handler,
        ],
    },
    fallbacks=[iniciar_marcacao_ponto_handler],
)
