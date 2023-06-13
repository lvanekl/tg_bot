import json
import random

import asyncio
import logging
import openai

from db.db_class import DB
from env import openai_token
from datetime import date as Date, time as Time

openai.api_key = openai_token

default_prompt = '''Я занимаюсь в спортсекции и я провожу голосование о сегодняшней тренировке, 
чтобы люди могли отметить планируют ли они сегодня прийти. По смыслу варианты ответа следующие: да, нет, не знаю. 
Твоя задача придумать вопрос и замены этим вариантам ответов, чтобы опросы не были однообразными. Атмосфера дружеская и в чате приветствуются подколы вплоть до самых жестких. 
Нужны варианты ответов в максимально шутливой форме - выдавай самые абсурдные и абстрактные варианты. Как можно меньше пафоса.
Запретные темы: тренер, пот, подружки, вторая половинка, энергетический напиток, железо, шест, всплыть, одна рука, вес, футбол. Я хочу получить ответ в формате json:
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
Обязательно сделай перепроверку на грамматические, фактические и речевые ошибки.'''


async def generate_poll(telegram_chat_id: int, chat_settings: dict, training: dict, my_db: DB) -> dict:
    print('hehehe')
    date, time, gym, sport = training['date'], training['time'], training['gym'], training['sport']

    funny_question, funny_yes_option, funny_maybe_option, funny_no_option, emoji = \
        chat_settings["funny_question"], chat_settings["funny_yes"], \
            chat_settings["funny_maybe"], chat_settings["funny_no"], chat_settings["emoji"]

    if any([funny_question, funny_yes_option, funny_maybe_option, funny_no_option]):
        loop = asyncio.get_event_loop()
        poll_variants = generate_poll_variants_using_chat_GPT(date, time, gym, sport)
        try:
            poll_variants = eval(poll_variants)
        except Exception as e:
            logging.error(e)
            poll_variants = {}
    else:
        poll_variants = await generate_poll_variants_using_db(telegram_chat_id, my_db=my_db)

    poll = choose_poll_variant(poll_variants)

    if emoji:
        poll = add_emoji(poll)

    if any([funny_question, funny_yes_option, funny_maybe_option, funny_no_option]):
        if funny_question:
            poll["question"] += f" ({date}, {time}, {gym})"
        else:
            poll["question"] = generate_default_question(date=date, time=time, gym=gym)

        if not funny_yes_option:
            poll["options"][0] = generate_default_yes_option(date=date, time=time, gym=gym)
        if not funny_maybe_option:
            poll["options"][1] = generate_default_maybe_option(date=date, time=time, gym=gym)
        if not funny_no_option:
            poll["options"][2] = generate_default_no_option(date=date, time=time, gym=gym)

    return poll


def generate_poll_variants_using_chat_GPT(date: Date, time: Time, gym: str, sport: str = "любой") -> str:
    prompt = default_prompt
    if sport is not None:
        prompt += f". ВАЖНО: вид спорта - {sport}, поэтому не используй другие виды спорта в генерации. " \
                  f"Кстати тренировка будет {date} в {time} в зале {gym} - если захочешь, " \
                  f"можешь использовать эти параметры в ответах"

    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}],
                                            max_tokens=2700)
    response = str(response)
    return json.loads(response)["choices"][0]["message"]["content"]


async def generate_poll_variants_using_db(telegram_chat_id: int, my_db: DB) -> dict:
    answer_alternatives_grouped_by_types = \
        await my_db.get_answer_alternatives_grouped_by_types(telegram_chat_id=telegram_chat_id)

    return answer_alternatives_grouped_by_types


def choose_poll_variant(poll_variants: dict) -> dict:
    # конструкция poll_variants.get("ключ", ["..."]) нужна,
    # чтобы даже если этого ключа нет в словаре, опрос не поломался
    question = random.choice(poll_variants.get("question", ["Идете сегодня на тренировку"]))
    yes_option = random.choice(poll_variants.get("yes", ["Планирую"]))
    maybe_option = random.choice(poll_variants.get("maybe", ["Возможно"]))
    no_option = random.choice(poll_variants.get("no", ["Нет("]))

    return {"question": question, "options": [yes_option, maybe_option, no_option]}


def add_emoji(poll_variants: dict) -> dict:
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


def generate_default_question(date: Date, time: Time, gym: str) -> str:
    templates = [f"Прийдете {date} в {time} на тренировку в {gym}?",
                 f"Как насчет тренировки в {gym} ({date} в {time})?",
                 f"Перекличка на тренировку в {gym} ({date} в {time})?",
                 f"Какие планы на вечер {date}? Есть опция собраться в {gym} в {time}"]

    return random.choice(templates)


def generate_default_yes_option(date: Date, time: Time, gym: str) -> str:
    templates = [f"Тренируюсь в {gym}",
                 f"Прийду",
                 f"+1",
                 f"Поддержу тренировку своим присутствием"]

    return random.choice(templates)


def generate_default_no_option(date: Date, time: Time, gym: str) -> str:
    templates = [f"Не прийду",
                 f"Занят чем-то бессмысленным и бесполезным",
                 f"Я ужасный человек и не иду сегодня на тренировку",
                 f"Неправильный вариант ответа",
                 "Нашел причину не идти сегодня (долго искал - пришлось придумать)"]

    return random.choice(templates)


def generate_default_maybe_option(date: Date, time: Time, gym: str) -> str:
    templates = [f"Пока в раздумьях",
                 f"Еще не решил",
                 f"хз",
                 f"Мой выбор между тренировкой и отдыхом зависит от победы апатии или энтузиазма"]

    return random.choice(templates)


async def main():
    # функция для тестирования генерируемых ответов
    db_path = ...
    my_db = DB(db_path)

    telegram_chat_id = 1111
    chat_settings = {"chat_GPT": True, "funny_question": True, "funny_yes": True, "funny_maybe": True,
                     "funny_no": True, "emoji": True}
    date = Date.today()
    time = Time(hour=19, minute=34)
    gym = "Акроритм"
    sport = "Спортивная гимнастика"

    training = {"date": date, "time": time, "gym": gym, "sport": sport}

    my_db.clear_all_tables()
    await my_db.new_chat(telegram_chat_id)
    await my_db.add_answer_alternative(telegram_chat_id=telegram_chat_id, answer_type="question",
                                       answer_value="Придете?")
    await my_db.add_answer_alternative(telegram_chat_id=telegram_chat_id, answer_type="yes", answer_value="Да")
    await my_db.add_answer_alternative(telegram_chat_id=telegram_chat_id, answer_type="maybe", answer_value="Мб")
    await my_db.add_answer_alternative(telegram_chat_id=telegram_chat_id, answer_type="no", answer_value="Нет")

    print(await generate_poll(telegram_chat_id,
                              chat_settings=chat_settings, training=training, db_path=db_path))
    my_db.clear_all_tables()


if __name__ == "__main__":
    main()
