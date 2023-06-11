import os

token = ""
openai_token = ""

DEFAULT_WELCOME_MEME_PATH = ""
DEFAULT_CHAT_GPT_FLAG = 0
DEFAULT_CHAT_FUNNY_QUESTION_FLAG = 0
DEFAULT_CHAT_FUNNY_YES_FLAG = 0
DEFAULT_CHAT_FUNNY_MAYBE_FLAG = 0
DEFAULT_CHAT_FUNNY_NO_FLAG = 0

TEST_DB_PATH = 'db/test.sqlite3'
DB_PATH = 'db/db.sqlite3'
DB_LOG_PATH = os.path.join('logs', 'db_log.log')
TESTING_LOG_PATH = os.path.join('logs', 'testing_log.log')
