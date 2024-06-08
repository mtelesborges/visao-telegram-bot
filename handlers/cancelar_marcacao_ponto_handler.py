from telegram import ReplyKeyboardRemove, Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from configs.const import BOTAO_CANCELAR
from configs.logger import logger


async def cancelar_marcacao_ponto(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    logger.info("Cancelando marcação...")
    user_data = context.user_data
    for key in user_data:
        user_data[key] = ""
    reply_markup = ReplyKeyboardRemove()
    await update.message.reply_text(
        text="Marcação cancelada com sucesso.", reply_markup=reply_markup
    )
    return ConversationHandler.END


cancelar_marcacao_ponto_handler = MessageHandler(
    filters.Regex(f"^{BOTAO_CANCELAR}$"), cancelar_marcacao_ponto
)
