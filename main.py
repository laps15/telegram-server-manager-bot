#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic inline bot example. Applies different text transformations.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
import logging
from uuid import uuid4

from telegram import InlineQueryResultArticle, ParseMode, InputTextMessageContent, Update
from telegram.ext import Updater, InlineQueryHandler, CommandHandler, CallbackContext
from telegram.utils.helpers import escape_markdown

import config
import security
from server import Server

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

server = Server(['ngrok', 'java'])
# server = Server(['notepad'])


def start(update: Update, context: CallbackContext) -> None:
    if security.authenticate_user(update.message.from_user.username, "start", logger):
        update.message.reply_text('Hi!')


def help_command(update: Update, context: CallbackContext) -> None:
    if security.authenticate_user(update.message.from_user.username, "help", logger):
        update.message.reply_text('Help!')


def status(update: Update, context: CallbackContext):
    if security.authenticate_user(update.message.from_user.username, "status", logger):
        server_status = "Server is currently " + server.get_status(True)
        update.message.reply_text(server_status)


def get_server_url_if_able(update: Update, context: CallbackContext):
    if security.authenticate_user(update.message.from_user.username, "server_url", logger):
        update.message.reply_text(server.get_server_url())


def stop_server_if_able(update: Update, context: CallbackContext):
    if security.authenticate_user(update.message.from_user.username, "stop_server", logger):
        should_use_force = "--force" in update.message.text
        success = server.stop_server(should_use_force)
        update.message.reply_text('Done!' if success else 'Could not stop server try the --force option')


def start_server_if_able(update: Update, context: CallbackContext):
    if security.authenticate_user(update.message.from_user.username, "start_server", logger):
        message = server.start_server()
        update.message.reply_text(message)



def main() -> None:
    updater = Updater(config.AUTH_TOKEN, use_context=True)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("status", status))
    dispatcher.add_handler(CommandHandler("server_url", get_server_url_if_able))
    dispatcher.add_handler(CommandHandler("stop_server", stop_server_if_able))
    dispatcher.add_handler(CommandHandler("start_server", start_server_if_able))

    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    # print(server.get_server_url())
    main()
