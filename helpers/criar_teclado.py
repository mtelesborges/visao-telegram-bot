from configs.const import (
    BOTAO_CANCELAR,
    BOTAO_LOCALIZACAO,
    BOTAO_FINALIZAR,
)
from telegram import KeyboardButton


def criar_teclado(tipo, mostrar_localizacao=True):
    if tipo == "group":
        return [
            # [BOTAO_CODIGO, BOTAO_FOTO],
            [BOTAO_FINALIZAR, BOTAO_CANCELAR],
        ]
    teclado = []
    if mostrar_localizacao is True:
        teclado.append(
            [
                KeyboardButton(
                    text=BOTAO_LOCALIZACAO,
                    request_location=True,
                    # callback_data=BOTAO_LOCALIZACAO,
                ),
                BOTAO_CANCELAR,
            ]
        )
    else:
        teclado.append(
            [BOTAO_FINALIZAR, BOTAO_CANCELAR],
        )
    return teclado
