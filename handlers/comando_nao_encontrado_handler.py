from telegram import Update
from telegram.ext import ContextTypes, MessageHandler, filters

from configs.const import COMANDOS_VALIDOS, MENSAGEM_COMANDO_NAO_LOCALIZADO


async def comando_nao_encontrado(update: Update, _: ContextTypes.DEFAULT_TYPE):
    comando = update.message.text
    if comando not in COMANDOS_VALIDOS:
        await update.message.reply_text(MENSAGEM_COMANDO_NAO_LOCALIZADO)


comando_nao_encontrado_handler = MessageHandler(
    filters.COMMAND, comando_nao_encontrado
)
