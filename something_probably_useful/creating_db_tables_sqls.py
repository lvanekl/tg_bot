all_create_statements = {"admin": '''CREATE TABLE IF NOT EXISTS "admin" (
	"id"	INTEGER NOT NULL UNIQUE,
	"chat"	INTEGER NOT NULL,
	"telegram_user_id"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("chat") REFERENCES "chat"("id") ON DELETE CASCADE
)''',
     "answer_alternative": '''CREATE TABLE IF NOT EXISTS "answer_alternative" (
	"id"	INTEGER NOT NULL UNIQUE,
	"chat"	INTEGER NOT NULL,
	"type"	TEXT NOT NULL,
	"value"	TEXT NOT NULL,
	FOREIGN KEY("chat") REFERENCES "chat"("id") ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
)''',
     "chat": '''CREATE TABLE IF NOT EXISTS "chat" (
	"telegram_chat_id"	INTEGER NOT NULL UNIQUE,
	PRIMARY KEY("telegram_chat_id")
)''',
     "chat_settings": '''CREATE TABLE IF NOT EXISTS "chat_settings" (
	"chat"	INTEGER NOT NULL UNIQUE,
	"welcome_meme"	TEXT,
	"chat_GPT"	INTEGER DEFAULT 0,
	"funny_question"	INTEGER DEFAULT 0,
	"funny_yes"	INTEGER DEFAULT 0,
	"funny_no"	INTEGER DEFAULT 0,
	"funny_maybe"	INTEGER DEFAULT 0,
	FOREIGN KEY("chat") REFERENCES "chat"("telegram_chat_id") ON DELETE CASCADE
)''',
     "gym": '''CREATE TABLE IF NOT EXISTS "gym" (
	"id"	INTEGER NOT NULL UNIQUE,
	"chat"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"address"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("chat") REFERENCES "chat"("id") ON DELETE CASCADE
)''',
     "meme": '''CREATE TABLE IF NOT EXISTS "meme" (
	"id"	INTEGER NOT NULL UNIQUE,
	"chat"	INTEGER NOT NULL,
	"picture_path"	TEXT NOT NULL,
	FOREIGN KEY("chat") REFERENCES "chat"("telegram_chat_id") ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
)''',
     "schedule": '''CREATE TABLE IF NOT EXISTS "schedule" (
	"id"	INTEGER NOT NULL UNIQUE,
	"chat"	INTEGER NOT NULL,
	"weekday"	INTEGER NOT NULL CHECK("weekday" >= 1 AND "weekday" <= 7),
	"sport"	TEXT NOT NULL,
	"gym"	INTEGER NOT NULL,
	"time"	TEXT NOT NULL,
	FOREIGN KEY("gym") REFERENCES "gym"("id") ON DELETE CASCADE,
	FOREIGN KEY("chat") REFERENCES "chat"("telegram_chat_id") ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
)''',
     "schedule_correction": '''CREATE TABLE IF NOT EXISTS "schedule_correction" (
	"id"	INTEGER NOT NULL UNIQUE,
	"chat"	INTEGER NOT NULL,
	"date_created"	INTEGER NOT NULL,
	"correction_type"	TEXT NOT NULL,
	"old_date"	TEXT,
	"old_time"	TEXT,
	"old_gym"	INTEGER,
	"new_date"	TEXT,
	"new_time"	TEXT,
	"new_gym"	INTEGER,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("chat") REFERENCES "chat"("id") ON DELETE CASCADE,
	FOREIGN KEY("new_gym") REFERENCES "gym"("id") ON DELETE CASCADE,
	FOREIGN KEY("old_gym") REFERENCES "gym"("id") ON DELETE CASCADE
)'''

     }
