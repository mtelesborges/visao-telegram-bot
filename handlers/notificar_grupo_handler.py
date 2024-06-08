from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    JobQueue,
    CallbackContext,
)
import dbf
from dateutil import parser
from datetime import datetime

from configs.const import COMANDO_REGISTRAR_NOTIFICACOES_GRUPO
from configs.logger import logger
from helpers.registrar_grupo import registrar_grupo


async def notificar_grupo(context: CallbackContext):
    codigo_grupo = context.job.data[0]
    nome_grupo = context.job.data[1]

    try:
        table = dbf.Table("./data/notificacoes.dbf")
        with table:
            procod_idx = table.create_index(
                lambda rec: (rec.CODGRUPO, rec.ENVIADA)
            )
            match = procod_idx.search(match=(codigo_grupo, 0))

            if len(match) == 0:
                logger.info(
                    f"Nenhuma notificação localizada para o grupo {nome_grupo}."  # noqa: E501
                )
                return []

            logger.info(
                f"Localizou-se {len(match)} notificações para o grupo {nome_grupo}."  # noqa: E501
            )
            for rec in match:
                data_notificacao = rec["DTNOTIFIC"]
                if parser.parse(data_notificacao) < datetime.now():
                    notificacao = rec["DSNOTIFIC"]
                    await context.bot.send_message(
                        chat_id=context.job.chat_id, text=notificacao
                    )
                    dbf.write(rec, ENVIADA=1)
    except Exception as erro:
        logger.error(
            f"Falha ao gerar notificação para o grupo {nome_grupo}.\n Erro: f{erro}"  # noqa: E501
        )


def iniciar_jobs_grupo(job_queue: JobQueue) -> None:
    table = dbf.Table("./data/grupos.dbf")
    with table:
        for row in table:
            registrar_job(job_queue, row["CODIGO"], row["NOME"])


def registrar_job(job_queue: JobQueue, codigo: int, nome: str):
    nome_grupo = f"G{codigo}".strip()
    jobs = job_queue.get_jobs_by_name(nome_grupo)
    if len(jobs) == 0:
        tempo_em_minutos = 60 * 15
        job_queue.run_repeating(
            notificar_grupo,
            tempo_em_minutos,
            data=[codigo, nome],
            chat_id=codigo,
            name=nome_grupo,
        )
        logger.info(f"Job cadastrado para o grupo {nome_grupo}")
    else:
        logger.info(f"Job já cadastrado para o grupo {nome_grupo}")


async def notificar(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    try:
        logger.info("Notificação em grupo...")
        logger.info(update.message.chat)

        nome = update.message.chat.title
        codigo = update.message.chat.id

        registrar_grupo(nome, codigo)
        registrar_job(context.job_queue, codigo, nome)

        await update.message.reply_text(
            f"Grupo {nome} registrado com sucesso.",  # noqa: E501
        )
    except Exception as e:
        logger.error(f"Erro ao registrar grupo:\n{e}")
        await update.message.reply_text(
            f"Erro ao registrar grupo:\n{e}",  # noqa: E501
        )
    return ConversationHandler.END


notificar_grupo_handler = CommandHandler(
    COMANDO_REGISTRAR_NOTIFICACOES_GRUPO, notificar
)
