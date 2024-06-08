from telegram import ReplyKeyboardRemove, Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler

from configs.const import COMANDO_CANCELAR
from configs.logger import logger


async def cancelar(update: Update, _: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("Restaurando...")
    reply_markup = ReplyKeyboardRemove()
    await update.message.reply_text(
        text="Configurações restauradas",
        reply_markup=reply_markup,
    )
    return ConversationHandler.END


cancelar_handler = CommandHandler(COMANDO_CANCELAR, cancelar)
