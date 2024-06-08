from datetime import datetime

import requests
from helpers.capturar_texto_foto import capturar_texto_foto
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ContextTypes, MessageHandler, filters

from configs.const import (
    BLOQUEAR_MARCACAO_DENTRO_INTERVALO_PROXIMO_PONTO,
    BOTAO_CANCELAR,
    BOTAO_CODIGO,
    BOTAO_FOTO,
    BOTAO_LOCALIZACAO,
    CHOOSING,
    INTERVALO_PROXIMO_PONTO_EM_MINUTOS,
    TYPING_REPLY,
)
from configs.logger import logger
from handlers.falha_ao_marcar_ponto import falha_ao_marcar_ponto
from helpers.burcar_horario_ultimo_ponto_funcionario import (
    burcar_horario_ultimo_ponto_funcionario,
)
from helpers.buscar_funcionario import buscar_funcionario
from helpers.criar_teclado import criar_teclado
from helpers.dict_to_str import dict_to_str
from helpers.diferenca_entre_horarios_em_minutos import (
    diferenca_entre_horarios_em_minutos,
)


async def salvar_dado_informado(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    try:
        user_data = context.user_data
        text = update.message.text
        category = user_data["choice"]
        logger.info("Salvando dados...")
        logger.info(user_data)

        if category == BOTAO_FOTO:
            fotos = update.message.photo

            if len(fotos) == 0:
                await update.message.reply_text(
                    "Nenhuma foto informada.\nPor favor, tente novamente.",
                    reply_markup=ReplyKeyboardMarkup(
                        criar_teclado(update.message.chat.type),
                        one_time_keyboard=True,
                    ),
                )
                return TYPING_REPLY

            foto = await context.bot.get_file(fotos[-1]["file_id"])
            file_unique_id = foto["file_unique_id"]
            ext = foto["file_path"].split(".")[-1]
            response = requests.get(foto["file_path"])

            path = f"{file_unique_id}.{ext}"
            text = path

            with open(f"./data/imgs/{path}", "wb") as f:
                f.write(response.content)
                logger.info(foto)

            user_data[category] = text
            del user_data["choice"]

            texto_foto = capturar_texto_foto(f"./data/imgs/{path}")
            logger.info(f"texto capturado na foto: {texto_foto}")
            user_data["texto_foto"] = texto_foto

            await update.message.reply_text(
                f"Dados informados: {dict_to_str(user_data)}\nPor favor, anexe sua localização.",  # noqa: E501
                reply_markup=ReplyKeyboardMarkup(
                    criar_teclado(update.message.chat.type),
                    one_time_keyboard=True,
                ),
            )

            user_data["choice"] = BOTAO_LOCALIZACAO

            return CHOOSING

        if category == BOTAO_CODIGO:
            if len(text) < 3:
                await update.message.reply_text(
                    f"O código informado não é válido: {text}.\nPor favor, tente novamente.",  # noqa: E501
                )
                return TYPING_REPLY

            codigo_empresa = text[:3]
            codigo_funcionario = text[3:]

            if (
                not codigo_empresa.isdigit()
                or not codigo_funcionario.isdigit()
            ):
                await update.message.reply_text(
                    f"O código informado não é válido: {text}.\nPor favor, tente novamente.",  # noqa: E501
                )
                return TYPING_REPLY

            try:
                funcionario = buscar_funcionario(
                    int(codigo_empresa), int(codigo_funcionario)
                )
                user_data["Nome"] = funcionario["NOMEFUN"]
            except Exception:
                await update.message.reply_text(
                    f"Funcionário não localizado: {text}.\nPor favor, tente novamente.",  # noqa: E501
                )
                return TYPING_REPLY

            horario_ultimo_ponto = burcar_horario_ultimo_ponto_funcionario(
                int(codigo_empresa), int(codigo_funcionario)
            )

            if horario_ultimo_ponto is not None:
                diferenca_em_minutos = diferenca_entre_horarios_em_minutos(
                    horario_ultimo_ponto, datetime.now()
                )

                if (
                    (diferenca_em_minutos < INTERVALO_PROXIMO_PONTO_EM_MINUTOS)
                    and BLOQUEAR_MARCACAO_DENTRO_INTERVALO_PROXIMO_PONTO == "S"
                ):
                    return await falha_ao_marcar_ponto(
                        update,
                        context,
                        f"Você bateu o ponto faz {diferenca_em_minutos} minutos.\nMarcação cancelada.",  # noqa: E501
                    )

            user_data[category] = text
            del user_data["choice"]

            await update.message.reply_text(
                f"Dados informados: {dict_to_str(user_data)}\nPor favor, anexe sua foto.",  # noqa: E501
            )

            user_data["choice"] = BOTAO_FOTO

            return TYPING_REPLY
    except Exception as erro:
        return await falha_ao_marcar_ponto(update, context, erro)


salvar_dado_informado_handler = MessageHandler(
    (filters.TEXT | filters.PHOTO | filters.LOCATION)
    & ~(filters.COMMAND | filters.Regex(f"^{BOTAO_CANCELAR}$")),
    salvar_dado_informado,
)
