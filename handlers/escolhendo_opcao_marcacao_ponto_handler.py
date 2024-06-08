from telegram import Update
from telegram.ext import ContextTypes

from configs.const import TYPING_REPLY
from configs.logger import logger


async def escolhendo_opcao_marcacao_ponto(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    logger.info("Selecionando uma opção...")
    text = update.message.text
    context.user_data["choice"] = text
    await update.message.reply_text(f"Informe o(a) {text.lower()}:")

    return TYPING_REPLY
