create_chat_table = '''CREATE TABLE  IF NOT EXISTS "chat" (
	"telegram_chat_id"	INTEGER NOT NULL UNIQUE,
	"welcome_meme"	TEXT,
	PRIMARY KEY("telegram_chat_id")
)'''

create_gym_table = '''CREATE TABLE IF NOT EXISTS "gym" (
	"id"	INTEGER NOT NULL UNIQUE,
	"chat"	INTEGER NOT NULL,
	"name"	TEXT NOT NULL,
	"address"	TEXT,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("chat") REFERENCES "chat"("telegram_chat_id") ON DELETE CASCADE
);'''

create_schedule_table = '''CREATE TABLE IF NOT EXISTS "schedule" (
	"id"	INTEGER NOT NULL UNIQUE,
	"chat"	INTEGER NOT NULL,
	"weekday"	INTEGER NOT NULL CHECK(weekday > 0 AND weekday <8),
	"sport"	TEXT NOT NULL,
	"gym"	INTEGER NOT NULL,
	"time"	TEXT NOT NULL,
	FOREIGN KEY("gym") REFERENCES "gym"("id") ON DELETE CASCADE,
	FOREIGN KEY("chat") REFERENCES "chat"("telegram_chat_id") ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
)'''

create_admin_table = '''CREATE TABLE IF NOT EXISTS "admin" (
	"id"	INTEGER NOT NULL UNIQUE,
	"chat"	INTEGER NOT NULL,
	"telegram_userid"	INTEGER NOT NULL,
	FOREIGN KEY("chat") REFERENCES "chat"("telegram_chat_id") ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);'''

create_meme_table = '''CREATE TABLE IF NOT EXISTS "meme" (
	"id"	INTEGER NOT NULL UNIQUE,
	"chat"	INTEGER NOT NULL,
	"picture_path"	TEXT NOT NULL,
	FOREIGN KEY("chat") REFERENCES "chat"("telegram_chat_id") ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);'''

create_schedule_correction_table = '''CREATE TABLE IF NOT EXISTS "schedule_correction" (
	"id"	INTEGER NOT NULL UNIQUE,
	"chat"	INTEGER NOT NULL,
	"type"	TEXT NOT NULL,
	"old_date"	TEXT,
	"old_time"	TEXT,
	"old_place"	INTEGER,
	"new_date"	TEXT,
	"new_time"	TEXT,
	"new_place"	INTEGER,
	FOREIGN KEY("chat") REFERENCES "chat"("telegram_chat_id") ON DELETE CASCADE,
	FOREIGN KEY("old_place") REFERENCES "gym"("id") ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("new_place") REFERENCES "gym"("id") ON DELETE CASCADE
);'''

create_answer_alternative_table = '''CREATE TABLE IF NOT EXISTS "answer_alternative" (
	"id"	INTEGER NOT NULL UNIQUE,
	"chat"	INTEGER NOT NULL,
	"type"	TEXT NOT NULL,
	"value"	TEXT NOT NULL,
	FOREIGN KEY("chat") REFERENCES "chat"("telegram_chat_id") ON DELETE CASCADE,
	PRIMARY KEY("id" AUTOINCREMENT)
);'''