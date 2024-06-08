from telegram import Update
from telegram.ext import (
    CommandHandler,
    ContextTypes,
    CallbackContext,
)
import dbf
from dateutil import parser
from datetime import datetime

from configs.const import COMANDO_NOTIFICAR
from configs.logger import logger


async def notificar(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    codigo_empresa: int,
    codigo_funcionario: int,
) -> int:
    try:
        logger.info("Notificando...")
        nome_job = f"F{codigo_empresa}{codigo_funcionario}"
        job = context.job_queue.get_jobs_by_name(nome_job)
        if len(job) != 0:
            logger.info(
                f"Job já cadastrado para o funcionário {codigo_empresa}{codigo_funcionario}"  # noqa: E501
            )
            return

        chat_id = update.message.chat_id
        tempo_em_minutos = 60 * 15
        context.job_queue.run_repeating(
            send_match_info,
            tempo_em_minutos,
            data=[codigo_empresa, codigo_funcionario],
            chat_id=chat_id,
            name=nome_job,
        )
    except Exception as erro:
        logger.error(
            f"Falha ao gerar notificação para o funcionário {codigo_empresa}{codigo_funcionario}.\n Erro: f{erro}"  # noqa: E501
        )


async def send_match_info(context: CallbackContext):
    codigo_empresa = int(context.job.data[0])
    codigo_funcionario = int(context.job.data[1])

    try:
        table = dbf.Table("./data/notificacoes.dbf")
        with table:
            procod_idx = table.create_index(
                lambda rec: (rec.EMPR, rec.CODFUN, rec.ENVIADA)
            )
            match = procod_idx.search(
                match=(codigo_empresa, codigo_funcionario, 0)
            )

            if len(match) == 0:
                logger.info(
                    f"Nenhuma notificação localizada para o funcionário código {codigo_funcionario}, empresa código {codigo_empresa}."  # noqa: E501
                )
                return []

            logger.info(
                f"Localizou-se {len(match)} notificações para o funcionário código {codigo_funcionario}, empresa código {codigo_empresa}."  # noqa: E501
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
            f"Falha ao gerar notificação para o funcionário {codigo_empresa}{codigo_funcionario}.\n Erro: f{erro}"  # noqa: E501
        )


notificar_handler = CommandHandler(COMANDO_NOTIFICAR, notificar)
