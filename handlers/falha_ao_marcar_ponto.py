from telegram import ReplyKeyboardRemove, Update
from telegram.ext import ContextTypes, ConversationHandler

from configs.logger import logger


async def falha_ao_marcar_ponto(
    update: Update, _: ContextTypes.DEFAULT_TYPE, erro: str
) -> int:
    logger.error(f"Falha ao marcar ponto\n{erro}")
    reply_markup = ReplyKeyboardRemove()
    await update.message.reply_text(
        text=f"Ocorreu um erro ao marcar seu ponto.\nErro: {erro}",
        reply_markup=reply_markup,
    )
    return ConversationHandler.END
