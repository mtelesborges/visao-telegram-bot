from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from configs.const import BOTAO_CODIGO, COMANDO_MARCAR_PONTO, TYPING_REPLY
from configs.logger import logger


async def iniciar_marcacao_ponto(
    update: Update, context: ContextTypes.DEFAULT_TYPE
):
    logger.info("Marcando ponto...")
    context.user_data["choice"] = BOTAO_CODIGO
    await update.message.reply_text(
        "Olá, por favor, informe seu código de funcionário"
    )
    return TYPING_REPLY


iniciar_marcacao_ponto_handler = CommandHandler(
    COMANDO_MARCAR_PONTO, iniciar_marcacao_ponto
)
