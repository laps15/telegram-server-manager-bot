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

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

import config
import security
from server import Server

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# server = Server([])
server = Server(config.process_names)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if security.authenticate_user(update.message.from_user.username, "start", logger):
        await update.message.reply_text('Hi!')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if security.authenticate_user(update.message.from_user.username, "help", logger):
        await update.message.reply_text('Help!')


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if security.authenticate_user(update.message.from_user.username, "status", logger):
        server_status = "Server is currently " + server.get_status(True)
        await update.message.reply_text(server_status)


async def get_server_url_if_able(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if security.authenticate_user(update.message.from_user.username, "server_url", logger):
        await update.message.reply_text(server.get_server_url())


async def stop_server_if_able(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if security.authenticate_user(update.message.from_user.username, "stop_server", logger):
        should_use_force = "--force" in update.message.text
        success = server.stop_server(should_use_force)
        await update.message.reply_text('Done!' if success else 'Could not stop server try the --force option')


async def start_server_if_able(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if security.authenticate_user(update.message.from_user.username, "start_server", logger):
        message = server.start_server()
        await update.message.reply_text(message)


async def run_backup_if_able(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if security.authenticate_user(update.message.from_user.username, "run_backup", logger):
        message = server.run_backup()
        await update.message.reply_text(message)



def main() -> None:
    app = ApplicationBuilder().token(config.AUTH_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("server_url", get_server_url_if_able))
    app.add_handler(CommandHandler("stop_server", stop_server_if_able))
    app.add_handler(CommandHandler("start_server", start_server_if_able))
    app.add_handler(CommandHandler("run_backup", run_backup_if_able))

    app.run_polling()


if __name__ == '__main__':
    # print(server.get_server_url())
    main()
