""" Este token autentica a integração com o Telegran """
# TOKEN = "5764755802:AAERmuY8hovuC-jjd4Iz4P55L-ZaV-b-zYo" # Teste
TOKEN = "5648582218:AAHpExjNDobAvncaPoB5E4jx-dV0FBYit-Y"  # Visio
#TOKEN = "5742713127:AAFO7gPWopAzOb9f_V3S8qyiG-MuE4W45Zo" # Visio Teste (Não usar)  # noqa: E501

"""
Esta lista será utilizada para alimentar o menu do bot seguindo o formato informado na documentação # noqa: E501
https://docs.python-telegram-bot.org/en/v20.0a4/telegram.bot.html#telegram.Bot.set_my_commands # noqa: E501
"""
COMANDO_AJUDA = "ajuda"
DESCRICAO_AJUDA = "Ajuda"

COMANDO_MARCAR_PONTO = "marcar_ponto"
DESCRICAO_MARCAR_PONTO = "Marcar Ponto"

COMANDO_CANCELAR = "cancelar"
DESCRICAO_CANCELAR = "Cancelar"

COMANDO_NOTIFICAR = "notificar"
DESCRICAO_NOTIFICAR = "Receber Notificações"

COMANDO_REGISTRAR_NOTIFICACOES_GRUPO = "registrar_notificacoes_grupo"
DESCRICAO_REGISTRAR_NOTIFICACOES_GRUPO = "Registrar Grupo para Notificações"

COMANDOS_VALIDOS = [
    COMANDO_AJUDA,
    COMANDO_MARCAR_PONTO,
    COMANDO_REGISTRAR_NOTIFICACOES_GRUPO,
]

MENU = [
    # (COMANDO_AJUDA, DESCRICAO_AJUDA),
    (COMANDO_MARCAR_PONTO, DESCRICAO_MARCAR_PONTO),
    (COMANDO_CANCELAR, DESCRICAO_CANCELAR),
    # (COMANDO_NOTIFICAR, DESCRICAO_NOTIFICAR),
]

MENU_GROUP = [
    (
        COMANDO_REGISTRAR_NOTIFICACOES_GRUPO,
        DESCRICAO_REGISTRAR_NOTIFICACOES_GRUPO,
    ),
]

MENSAGEM_COMANDO_NAO_LOCALIZADO = "Desculpe, não entendi o comando digitado, poderia tentar novamente?\nDigite /ajuda para listar as opções disponíveis."  # noqa: E501

CHOOSING, TYPING_REPLY, TYPING_CHOICE, CANCELAR = range(4)

BOTAO_CODIGO = "Código"
BOTAO_FOTO = "Foto"
BOTAO_FINALIZAR = "Finalizar"
BOTAO_CANCELAR = "Cancelar"
BOTAO_LOCALIZACAO = "Localização"

"""
O intervalo para o próximo ponto deve ser especificado em minutos
É responsável por indicar o tempo mínimo para a próxima marcação
"""
INTERVALO_PROXIMO_PONTO_EM_MINUTOS = 15

BLOQUEAR_MARCACAO_DENTRO_INTERVALO_PROXIMO_PONTO = "N"


INTERVALO_MARCACAO_FORA_TURNO_EM_MINUTOS = 120

"""
Esta configuração informa se a marcação de ponto deve ser bloqueada quando a marcação ocorre antes da expiração do tempo definido na variável INTERVALO_MARCACAO_FORA_TURNO_EM_MINUTOS # noqa: E501
"""
BLOQUEAR_MARCACAO_FORA_TURNO = "N"

"""
Esta opção habilita a validação da obrigatoriedade de preenchimento da localização # noqa: E501
Observação: o Telegram não permite compartilhamento de localização em grupos # noqa: E501
"""
OBRIGAR_USO_LOCALIZACAO = "N"

FOLDER_ROOT = "C:\\Users\\teles\\Projetos\\visio-telegram-bot"
