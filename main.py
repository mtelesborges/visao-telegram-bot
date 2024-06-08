from configs.menu import configurar_menu
from telegram.ext import Application

from configs.const import TOKEN
from handlers.informar_dados_ponto_handler import informar_dados_ponto_handler
from handlers.cancelar_handler import cancelar_handler
from handlers.notificar_handler import notificar_handler
from handlers.notificar_grupo_handler import (
    notificar_grupo_handler,
    iniciar_jobs_grupo,
)


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = (
        Application.builder().token(TOKEN).post_init(configurar_menu).build()
    )

    application.add_handler(informar_dados_ponto_handler)
    application.add_handler(cancelar_handler)
    application.add_handler(notificar_handler)
    application.add_handler(notificar_grupo_handler)

    iniciar_jobs_grupo(application.job_queue)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
