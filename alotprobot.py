#!/usr/bin/env python
# -*- coding: utf-8 -*-


import configparser
import datetime
import logging
from time import sleep
from commands import *
import re
import requests
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot, ChatAction, Update, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, ConversationHandler, \
    RegexHandler

from peewee import *

from dbpewee import Users, CallRecords

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

database = SqliteDatabase('alotpro.db')

logger = logging.getLogger(__name__)
CHOOSING, TYPING_CHOICE, TYPING_REPLY, OTHER = range(4)

config = configparser.ConfigParser()
config.read('bot.ini')

APIKEY = config['KEYS']['bot_apikey']


def create_tables():
    with database:
        database.create_tables([Users, CallRecords])


def main():
    # Create the Updater and pass it your bot's token.
    config = configparser.ConfigParser()
    config.read('bot.ini')
    updater = Updater(token=APIKEY)
    dsp = updater.dispatcher

    dsp.add_handler(CommandHandler('start', start))
    dsp.add_handler(CommandHandler('help', help))
    dsp.add_handler(CommandHandler('setup', setup))
    dsp.add_handler(CommandHandler('initconv', initconv))
    dsp.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))

    dsp.add_handler(MessageHandler(Filters.all, echo))

    dsp.add_handler(CallbackQueryHandler(help_main_menu, pattern="help_main_menu"))
    dsp.add_handler(CallbackQueryHandler(help_main_menu, pattern='help_back'))
    dsp.add_handler(CallbackQueryHandler(button, pass_update_queue=True,
                                         pass_user_data=True,
                                         ))

    # Add conversation handler with the states CHOOSING, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('initconv', initconv)],

        states={
            CHOOSING: [RegexHandler('^(Button 1|Button 2|Other)$',
                                    regular_choice,
                                    pass_user_data=True),
                       RegexHandler('^Something else...$',
                                    custom_choice),
                       ],

            TYPING_CHOICE: [MessageHandler(Filters.text,
                                           regular_choice,
                                           pass_user_data=True),
                            ],

            TYPING_REPLY: [MessageHandler(Filters.text,
                                          received_information,
                                          pass_user_data=True),
                           ],
        },

        fallbacks=[RegexHandler('^Done$', done, pass_user_data=True)]
    )

    # updater.dispatcher.add_handler(conv_handler)

    updater.dispatcher.add_error_handler(error)
    # Start the Bot
    webhook = config['WEBHOOK']

    if webhook:
        updater.start_webhook(listen=webhook['listen'], port=webhook['port'], url_path=APIKEY)
        updater.bot.set_webhook(webhook_url=webhook['url'] + '/' + APIKEY,
                                certificate=open(webhook['certificate'], 'rb'))
    else:
        updater.start_polling(timeout=30, poll_interval=4)
    # Run the bot until the user presses Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT
    updater.idle()


if __name__ == '__main__':
    create_tables()
    main()
