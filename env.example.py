import os

token = ""
openai_token = ""

DEFAULT_WELCOME_MEME_PATH = None
DEFAULT_CHAT_GPT_FLAG = 0
DEFAULT_CHAT_FUNNY_YES_FLAG = 0
DEFAULT_CHAT_FUNNY_QUESTION_FLAG = 0

DB_PATH = 'db/db.sqlite3'
DB_LOG_PATH = os.path.join('logs', 'db_log.log')
TESTING_LOG_PATH = os.path.join('logs', 'testing_log.log')

