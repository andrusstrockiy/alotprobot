import json
from datetime import datetime
import telegram
import requests
import configparser
from time import sleep
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot, ChatAction, Update, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
config = configparser.ConfigParser()
config.read('bot.ini')
APIKEY = config['KEYS']['bot_apikey']


def start(bot: Bot, update: Update):
    logger.info("Bot started")
    logger.info("Api key %s" % APIKEY)
    if update.message.chat_id is None:
        bot.sendContact(chat_id=)
    bot.sendChatAction(chat_id=update.message.chat_id, action=ChatAction.TYPING)
    sleep(0.2)
    keyboard = [[InlineKeyboardButton("SetFilters", callback_data='filters'),
                 InlineKeyboardButton("Help", callback_data='help_main_menu')],
                [InlineKeyboardButton("Inline",
                                      # callback_data='3',
                                      # switch_inline_query='andruss Cancel',
                                      switch_inline_query_current_chat="chat andruss",
                                      )]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def echo(bot, update):
    logger.info("Message data to echo function {}".format(update.message))
    logger.info("Bot data {}".format(bot))


def help_main_menu(bot: Bot, update: Update):
    callquery = update.callback_query
    logger.info("Help Main Menu {}".format(update))
    logger.info("Msg id {}".format(callquery.message.message_id))
    bot.delete_message(chat_id=callquery.message.chat.id,
                       message_id=callquery.message.message_id)
    button_list = [[
        InlineKeyboardButton("Help_Back", callback_data="help_back"),
        InlineKeyboardButton("Help_Forward", callback_data="help_forward")],
        [InlineKeyboardButton("Quit", callback_data="quit")]
    ]
    reply_markup = InlineKeyboardMarkup(button_list)

    bot.send_message(text="Help Menu", reply_markup=reply_markup, chat_id=callquery.message.chat.id)

    # update.message.reply_text("Make your choice", reply_markup=reply_markup)


def button(bot, update, user_data, update_queue):
    query = update.callback_query
    # mod_match = re.match(r"help_module\((.+?)\)", query.data)
    # prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    # next_match = re.match(r"help_next\((.+?)\)", query.data)
    # back_match = re.match(r"help_back", query.data)
    logger.info("update queue {}".format(update_queue))
    logger.info('{} query user data {}'.format(__name__, query))
    logger.info('query message {} and chat_id {}'.format(query.message, query.chat_instance))
    # user = update.message.from_user
    # bot.edit_message_text(text="Selected option: {} mid {}".format(query.data,
    #                                                                query.message.message_id),
    #                       chat_id=query.message.chat_id,
    #                       message_id=query.message.message_id)
    logger.info("button data : {}  and user data :{}".format(query.data, user_data))
    if query.data == 'help_module':
        chat = update.effective_chat
        logger.info("Chait {}".format(chat))
        # update.message.reply_text('Please make your choice')
        help_main_menu(bot, update, chat)
    if query.data == 'help_back':
        chat = query.chat_instance
        logger.info("Chatid Help_back {}".format(chat))
        help_main_menu(bot, update, chat)
    else:
        update.message.reply_text("Unknown Command")


def setup(args):
    pass


def initconv(args):
    pass


def welcome(bot, update):
    msg = update.effective_message
    chat = update.effective_message
    usr = update.effective_user

    for u in msg.new_chat_members:
        bot.send_message(chat.id, "Welcome {} to {} "
                                  "Please read the "
                                  "pinned message.".format(u.mention_html(), chat.title),
                         parse_mode='HTML')


def regular_choice(args):
    pass


def custom_choice(args):
    pass


def received_information(args):
    pass


def done(args):
    pass


def help(bot: Bot, update: Update) -> None:
    button_list = [[
        InlineKeyboardButton("col1", callback_data=1),
        InlineKeyboardButton("col2", callback_data=2)],
        [InlineKeyboardButton("row 2", callback_data=3)]
    ]
    reply_markup = InlineKeyboardMarkup(button_list)
    update.message.reply_text("Make your choice", reply_markup=reply_markup)
    # update.message.reply_text(text='Please make your choice')
