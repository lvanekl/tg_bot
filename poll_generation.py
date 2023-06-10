import json
import random
import openai

from db.db_class import DB
from env import openai_token, DB_PATH
from datetime import date as Date, time as Time

openai.api_key = openai_token

my_prompt = '''Я занимаюсь в спортсекции и я провожу голосование о сегодняшней тренировке, 
чтобы люди могли отметить планируют ли они сегодня прийти. По смыслу варианты ответа следующие: да, нет, не знаю. 
Твоя задача придумать вопрос и замены этим вариантам ответов, чтобы опросы не были однообразными. Атмосфера дружеская и в чате приветствуются подколы вплоть до самых жестких. 
Нужны варианты ответов в максимально шутливой форме - выдавай самые абсурдные и абстрактные варианты. Как можно меньше пафоса.
Запретные темы: тренер, пот, подружки, вторая половинка, энергетический напиток, железо, шест, всплыть, одна рука, вес. Я хочу получить ответ в формате json:
{"question": ["", "", ""], "yes": ["", "", ""], "maybe": ["", "", ""], "no": ["", "", ""], ]}. 
Вот тебе примеры хороших вариантов,  {
  "да": [
    "Я приду и покажу всем, как сделать отжимание на одной руке, держа бутерброд в другой",
    "Да, сегодня я буду участвовать в спортивной эпопее!",
    "Да, я настроен так серьезно, что мои мышцы уже начали набирать массу, только думая об этой тренировке!",
  ],
  "нет": [
    "Не сегодня, я решил(а) превратиться в картофельное чипсовое лежебоко",
    "Нет, я официально объявляю себя чемпионом по совмещению диванной и телевизионной гимнастики",
    "Я собираюсь сидеть и вынашивать новые спортивные идеи в покое.",
    "Нет, моя энергия будет направлена на увеличение попкорна в своем организме.",
    "Сегодня я не приду, потому что меня похитили пришельцы и они требуют, чтобы я им показал, как пропускать тренировки.",
    "Нет, сегодня я занят чем-то ненужным и бессмысленным".
  ],
  "не знаю": [
    "Я на грани решения между тренировкой и занятием мастерством подушечного боя",
    "Моя предвыборная кампания между тренировкой и отдыхом зависит от победы апатии или энтузиазма."
  ]
}

НО ИХ ТЕБЕ КОПИРОВАТЬ НЕЛЬЗЯ. Придумай сам, мне нужны именно новые варианты ответов
Обязательно сделай перепроверку на грамматические, фактические и речевые ошибки'''

my_db = DB(DB_PATH)


def generate_poll(telegram_chat_id: int, date: Date, time: Time, place: str):
    # chatGPT, funny_yes_option, funny_question, emoji = True, False, False, False

    chat_settings = my_db.get_chat_settings(telegram_chat_id=telegram_chat_id)[0]
    chat_GPT, funny_yes_option, funny_question, emoji = chat_settings["chat_GPT"], chat_settings["funny_yes_option"], \
        chat_settings["funny_question"], chat_settings["emoji"]

    if chat_GPT:
        poll_variants = generate_poll_variants_chat_GPT()
        poll_variants = eval(poll_variants)
        print(poll_variants)
    else:
        poll_variants = generate_poll_variants_using_db(telegram_chat_id)

    poll = choose_poll_variant(poll_variants)

    if emoji:
        poll = add_emoji(poll_variants)

    if funny_question:
        poll["question"] += f" ({date}, {time}, {place})"
    else:
        poll["question"] = generate_default_question(date=date, time=time, place=place)

    if not funny_yes_option:
        poll["options"][0] = generate_default_yes_option(date=date, time=time, place=place)

    return poll


def generate_poll_variants_chat_GPT():
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": my_prompt}],
                                            max_tokens=2700)
    content = str(response)
    return json.loads(content)["choices"][0]["message"]["content"]


def generate_poll_variants_using_db(telegram_chat_id: int):
    answer_alternatives_grouped_by_types = \
        my_db.get_answer_alternatives_grouped_by_types(telegram_chat_id=telegram_chat_id)

    return answer_alternatives_grouped_by_types


def choose_poll_variant(poll_variants):
    question = random.choice(poll_variants["question"])
    yes_option = random.choice(poll_variants["yes"])
    maybe_option = random.choice(poll_variants["maybe"])
    no_option = random.choice(poll_variants["no"])

    return {"question": question, "options": [yes_option, maybe_option, no_option]}


def add_emoji(poll_variants):
    emoji_variants = ["✅🌀💤",
                      "🥳🧐🫡",
                      "👍✌️👋",
                      "😎😐🫥",
                      "❤️❓💔",
                      "💯❓⁉️", ]
    em = random.choice(emoji_variants)

    poll_variants["options"][0] = em[0] + poll_variants["options"][0]
    poll_variants["options"][1] = em[1] + poll_variants["options"][1]
    poll_variants["options"][2] = em[2] + poll_variants["options"][2]

    return poll_variants


def generate_default_question(date: Date, time: Time, place: str):
    templates = [f"Прийдете {date} в {time} на тренировку в {place}?",
                 f"Как насчет тренировки в {place} ({date} в {time})?",
                 f"Перекличка на тренировку в {place} ({date} в {time})?",
                 f"Какие планы на вечер {date}? Есть опция собраться в {place} в {time}"]

    return random.choice(templates)


def generate_default_yes_option(date: Date, time: Time, place: str):
    templates = [f"Тренируюсь в {place}?",
                 f"Прийду",
                 f"+1",
                 f"Поддержу тренировку своим присутствием"]

    return random.choice(templates)


if __name__ == "__main__":
    print(generate_poll(True))
