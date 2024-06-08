from datetime import datetime

from dbf import NotFoundError
from handlers.notificar_handler import notificar
from helpers.registrar_ponto_espelho import registrar_ponto_espelho
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler

from configs.const import (
    BLOQUEAR_MARCACAO_FORA_TURNO,
    BOTAO_CODIGO,
    BOTAO_FINALIZAR,
    BOTAO_FOTO,
    BOTAO_LOCALIZACAO,
    CHOOSING,
    INTERVALO_MARCACAO_FORA_TURNO_EM_MINUTOS,
    OBRIGAR_USO_LOCALIZACAO,
)
from configs.logger import logger
from handlers.falha_ao_marcar_ponto import falha_ao_marcar_ponto
from helpers.buscar_funcionario import buscar_funcionario
from helpers.buscar_turno_funcionario import buscar_turno_funcionario
from helpers.criar_teclado import criar_teclado
from helpers.registrar_ponto import registrar_ponto


async def finalizar_marcacao_ponto(
        update: Update, context: ContextTypes.DEFAULT_TYPE
):
    try:
        logger.info("Finalizando marcação...")
        user_data = context.user_data

        if BOTAO_CODIGO not in user_data:
            await update.message.reply_text(
                "Preencha o código do funcionário antes de finalizar ou cancele a execução.",  # noqa: E501
            )
            return CHOOSING

        if BOTAO_FOTO not in user_data:
            await update.message.reply_text(
                "Preencha a foto antes de finalizar ou cancele a execução.",
            )
            return CHOOSING

        if (
                BOTAO_LOCALIZACAO not in user_data
                and OBRIGAR_USO_LOCALIZACAO == "S"
        ):
            await update.message.reply_text(
                "Preencha a localização antes de finalizar ou cancele a execução.",  # noqa: E501
                reply_markup=ReplyKeyboardMarkup(
                    criar_teclado(update.message.chat.type),
                    one_time_keyboard=True,
                ),
            )
            return CHOOSING

        text = user_data[BOTAO_CODIGO]
        codigo_empresa = text[:3]
        codigo_funcionario = text[3:]
        localizacao = ""
        texto_foto = ""
        if BOTAO_LOCALIZACAO in user_data:
            localizacao = user_data[BOTAO_LOCALIZACAO]
        if "texto_foto" in user_data:
            texto_foto = user_data["texto_foto"]
        nome = user_data["Nome"]
        foto = user_data[BOTAO_FOTO]

        if not codigo_empresa.isdigit() or not codigo_funcionario.isdigit():
            await update.message.reply_text(
                f"O código informado não é válido: \
                    {text}.\nPor favor, tente novamente.",
            )
            return CHOOSING

        try:
            buscar_funcionario(int(codigo_empresa), int(codigo_funcionario))
        except NotFoundError:
            await update.message.reply_text(
                f"Funcionário não localizado: \
                    {text}.\nPor favor, tente novamente.",
            )
            return CHOOSING

        try:
            horarios = buscar_turno_funcionario(
                int(codigo_empresa), int(codigo_funcionario)
            )
        except Exception:
            await update.message.reply_text(
                f"Nenhum turno de trabalho localizado: \
                    {text}.\nPor favor, tente novamente.",
                reply_markup=ReplyKeyboardMarkup(
                    criar_teclado(update.message.chat.type),
                    one_time_keyboard=True,
                ),
            )
            return CHOOSING

        now = datetime.now()
        hora_atual_em_decimal = now.hour + (now.minute / 60)
        horario_turno = [
            horario for horario in horarios if horario > hora_atual_em_decimal
        ]

        if len(horario_turno) == 0:
            horario_turno = horarios[-1]
        else:
            horario_turno = horario_turno[0]

        diferenca_horario = int((hora_atual_em_decimal - horario_turno) * 60)

        if (
                abs(diferenca_horario) >= INTERVALO_MARCACAO_FORA_TURNO_EM_MINUTOS
        ) and BLOQUEAR_MARCACAO_FORA_TURNO == "S":
            await update.message.reply_text(
                f"O horário atual excede o seu turno em {diferenca_horario} minutos.\nPor favor, procure seu gestor.",
                # noqa: E501
                reply_markup=ReplyKeyboardMarkup(
                    criar_teclado(update.message.chat.type),
                    one_time_keyboard=True,
                ),
            )

            return CHOOSING

        observacao = None

        if (
                abs(diferenca_horario) >= INTERVALO_MARCACAO_FORA_TURNO_EM_MINUTOS
        ) and BLOQUEAR_MARCACAO_FORA_TURNO == "N":
            observacao = f"O horario atual excede o seu turno em {diferenca_horario} minutos."  # noqa: E501

        if localizacao is None:
            localizacao = ""

        if texto_foto is None:
            texto_foto = ""

        registrar_ponto(
            codigo_empresa,
            codigo_funcionario,
            str(datetime.now()),
            observacao,
            foto,
            localizacao,
            texto_foto,
        )

        registrar_ponto_espelho(int(codigo_empresa), int(codigo_funcionario), datetime.now())

        reply_markup = ReplyKeyboardRemove()

        for key in user_data:
            user_data[key] = ""

        await notificar(update, context, codigo_empresa, codigo_funcionario)

        await update.message.reply_text(
            text=f"{nome.strip()}, seu ponto foi registrado!",
            reply_markup=reply_markup,
        )

        return ConversationHandler.END

    except Exception as erro:
        return await falha_ao_marcar_ponto(update, context, erro)


finalizar_marcacao_ponto_handler = CommandHandler(
    BOTAO_FINALIZAR, finalizar_marcacao_ponto
)
