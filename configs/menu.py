from telegram.ext import Application
from telegram import (
    BotCommandScopeAllPrivateChats,
    BotCommandScopeAllGroupChats,
)
from configs.const import MENU, MENU_GROUP


async def configurar_menu(application: Application) -> None:
    await application.bot.set_my_commands(
        MENU, scope=BotCommandScopeAllPrivateChats()
    )
    await application.bot.set_my_commands(
        MENU_GROUP, scope=BotCommandScopeAllGroupChats()
    )
