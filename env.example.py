import logging
import os
from datetime import time as Time

token = ""
openai_token = ""

NEW_CHAT_MEME_PATH = "media/new_chat_meme.jpg"
DEFAULT_WELCOME_MEME_PATH = ""
DEFAULT_AUTO_POLL_FLAG = 1
DEFAULT_CHAT_FUNNY_QUESTION_FLAG = 1
DEFAULT_CHAT_FUNNY_YES_FLAG = 1
DEFAULT_CHAT_FUNNY_MAYBE_FLAG = 1
DEFAULT_CHAT_FUNNY_NO_FLAG = 1
DEFAULT_CHAT_EMOJI_FLAG = 1
DEFAULT_POLL_SEND_TIME = Time(hour=7)
DEFAULT_EVERYONE_IS_ADMIN = 0
DEFAULT_LANGUAGE = 'Русский'

TEST_DB_PATH = 'db/test.sqlite3'
DB_PATH = 'db/db.sqlite3'
LOG_PATH = os.path.join('logs', 'log.log')
LOGGING_LEVEL = logging.DEBUG

DEVELOPER_TELEGRAM_ID = 0
SCHEDULE_CHECK_RUN_TIME = Time(hour=1, minute=41)
BOT_USERNAME = "@Igor2_bot"
