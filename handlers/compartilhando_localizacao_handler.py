from geopy.geocoders import Nominatim
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes

from configs.const import BOTAO_LOCALIZACAO, CHOOSING
from configs.logger import logger
from helpers.criar_teclado import criar_teclado
from helpers.dict_to_str import dict_to_str


async def compartilhando_localizacao(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    logger.info("Compartilhando localização...")
    user_data = context.user_data
    localizacao = update.message.location
    user_data[BOTAO_LOCALIZACAO] = ""
    if localizacao is not None:
        try:
            geolocator = Nominatim(user_agent="coordinateconverter")
            user_data[BOTAO_LOCALIZACAO] = geolocator.reverse(
                f"{localizacao.latitude}, {localizacao.longitude}"
            ).address
        except Exception as erro:
            logger.error(f"Erro ao consultaro endereço.\n {erro}")
    del user_data["choice"]
    await update.message.reply_text(
        f"Dados informados: {dict_to_str(user_data)}",
        reply_markup=ReplyKeyboardMarkup(
            criar_teclado(update.message.chat.type, False),
            one_time_keyboard=True,
        ),
    )

    user_data["choice"] = ""

    return CHOOSING
