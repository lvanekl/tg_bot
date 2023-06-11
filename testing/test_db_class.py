import asyncio
import pytest
# import logging

from db.db_class import DB
from env import TEST_DB_PATH, DEFAULT_WELCOME_MEME_PATH, \
    DEFAULT_CHAT_GPT_FLAG, DEFAULT_CHAT_FUNNY_YES_FLAG, DEFAULT_CHAT_FUNNY_QUESTION_FLAG, \
    DEFAULT_CHAT_FUNNY_NO_FLAG, DEFAULT_CHAT_FUNNY_MAYBE_FLAG



@pytest.mark.asyncio
@pytest.mark.parametrize("chats_amount, tg_chats_ids", [(1, [11111]), (2, [1111, 2222]), (3, [111, 222, 333])])
async def test_new_chat(chats_amount, tg_chats_ids):
    # Этот тест проверяет методы new_chat, get_chats, get_chat_settings
    my_db = DB(TEST_DB_PATH)

    my_db.clear_all_tables()

    for i in range(chats_amount):
        await my_db.new_chat(telegram_chat_id=tg_chats_ids[i])

    chats = await my_db.get_chats()

    assert len(chats) == chats_amount
    assert [chat['telegram_chat_id'] for chat in chats] == tg_chats_ids

    chats_settings = [await my_db.get_chat_settings(chat_id) for chat_id in tg_chats_ids]

    assert len(chats_settings) == chats_amount

    assert [[{"chat": chat_id, "welcome_meme": DEFAULT_WELCOME_MEME_PATH, "chat_GPT": DEFAULT_CHAT_GPT_FLAG,
              "funny_yes": DEFAULT_CHAT_FUNNY_YES_FLAG, "funny_question": DEFAULT_CHAT_FUNNY_QUESTION_FLAG,
              "funny_no": DEFAULT_CHAT_FUNNY_NO_FLAG, "funny_maybe": DEFAULT_CHAT_FUNNY_MAYBE_FLAG}]
            for chat_id in tg_chats_ids] == chats_settings

    # кажется чаты и настройки к ним создаются правильно
    my_db.clear_all_tables()


@pytest.mark.asyncio
@pytest.mark.parametrize("chat_id, kwargs", [(11111, {}),
                                             (22222, {'welcome_meme': '1.jpg'}),
                                             (33333, {'welcome_meme': ''}),
                                             (44444, {'chat_GPT': 1, "funny_yes": 1, "funny_question": 0}),
                                             (55555, {'chat_GPT': 0, "funny_yes": 0, "funny_question": 1})])
async def test_edit_chat_settings(chat_id, kwargs):
    # Этот тест проверяет методы edit_chat_settings, get_chat_settings
    my_db = DB(TEST_DB_PATH)
    my_db.clear_all_tables()
    await my_db.new_chat(telegram_chat_id=chat_id)

    await my_db.edit_chat_settings(chat_id, **kwargs)
    settings = (await my_db.get_chat_settings(chat_id))[0]

    assert settings['chat'] == chat_id

    settings_edited_fields = {}

    for key, value in settings.items():
        if key in kwargs:
            settings_edited_fields[key] = value

    assert settings_edited_fields == kwargs
    # думаю что все норм
    my_db.clear_all_tables()


def test_add_get_remove_gym():
    # Этот тест проверяет методы get_gyms, add_gym, remove_gym
    my_db = DB(TEST_DB_PATH)
    my_db.clear_all_tables()

    my_db.clear_all_tables()


def test_edit_gym():
    # Этот тест проверяет методы get_gyms, add_gym, edit_gym
    my_db = DB(TEST_DB_PATH)
    my_db.clear_all_tables()

    my_db.clear_all_tables()


def test_add_get_remove_schedule():
    # Этот тест проверяет методы
    my_db = DB(TEST_DB_PATH)
    my_db.clear_all_tables()

    my_db.clear_all_tables()


def test_edit_schedule():
    # Этот тест проверяет методы
    my_db = DB(TEST_DB_PATH)
    my_db.clear_all_tables()

    my_db.clear_all_tables()


def test_add_get_remove_schedule_correction():
    # Этот тест проверяет методы
    my_db = DB(TEST_DB_PATH)
    my_db.clear_all_tables()

    my_db.clear_all_tables()


def test_edit_schedule_correction():
    # Этот тест проверяет методы
    my_db = DB(TEST_DB_PATH)
    my_db.clear_all_tables()

    my_db.clear_all_tables()


def test_add_get_remove_admin():
    # Этот тест проверяет методы
    my_db = DB(TEST_DB_PATH)
    my_db.clear_all_tables()

    my_db.clear_all_tables()


def test_add_get_remove_answer_alternative():
    # Этот тест проверяет методы
    my_db = DB(TEST_DB_PATH)
    my_db.clear_all_tables()

    my_db.clear_all_tables()


def test_add_get_remove_answer_alternatives_grouped_by_types():
    # Этот тест проверяет методы
    my_db = DB(TEST_DB_PATH)
    my_db.clear_all_tables()

    my_db.clear_all_tables()


def old_testing():
    my_db = DB(TEST_DB_PATH)
    # очистка базы данных
    print(my_db.clear_all_tables())
    # создание нового чата
    print(my_db.new_chat(telegram_chat_id=1111111))

    # проверим пустая ли бд
    assert my_db.get_gyms(telegram_chat_id=1111111) == [], \
        "база данных не пустая, для данного чата уже есть данные в бд"

    # создаем 4 зала
    my_db.add_gym(telegram_chat_id=1111111, name="gym1")
    my_db.add_gym(telegram_chat_id=1111111, name="gym2")
    my_db.add_gym(telegram_chat_id=1111111, name="gym3")
    my_db.add_gym(telegram_chat_id=1111111, name="gym4")
    current_gyms1 = my_db.get_gyms(telegram_chat_id=1111111)

    # проверяем что их 4
    # print(current_gyms1)
    assert len(current_gyms1) == 4, "неверное колво current_gyms1"

    # достанем айдишники новых залов
    g1 = current_gyms1[0][0]
    g2 = current_gyms1[1][0]
    g3 = current_gyms1[2][0]
    g4 = current_gyms1[3][0]

    # удалим третий
    my_db.remove_gym(g3)
    current_gyms2 = my_db.get_gyms(telegram_chat_id=1111111)

    # проверим что такая же длина и содержание
    # print(current_gyms2)
    assert len(current_gyms2) == 3, "неверное колво current_gyms2"
    assert current_gyms2 == current_gyms1[:2] + [current_gyms1[3]], \
        "неверное содержание current_gyms2"

    # проверим как работает редактирование
    m_g1 = my_db.edit_gym(g1, name="gggym1")
    m_g2 = my_db.edit_gym(g2, address="address2")
    m_g3 = my_db.edit_gym(g4, name="gggym4", address="address4")
    m_g4 = my_db.edit_gym(g1)

    # TODO добавить assert на содержание текущего набота залов
    current_gyms3 = my_db.get_gyms(telegram_chat_id=1111111)
    # print(m_g1, m_g2, m_g3, m_g4, sep='\n')
    # print(current_gyms3)

    # проверяем работоспособность расписания
    # создадим расписание
    my_db.add_schedule(telegram_chat_id=1111111, weekday=1, sport="s1", gym=g1, time="19.30")
    my_db.add_schedule(telegram_chat_id=1111111, weekday=5, sport="s2", gym=g3, time="19.30")
    my_db.add_schedule(telegram_chat_id=1111111, weekday=7, sport="s3", gym=g4, time="19.30")
    my_db.add_schedule(telegram_chat_id=1111111, weekday=2, sport="s1", gym=g1, time="19.30")
    current_sh1 = my_db.get_schedule(telegram_chat_id=1111111)

    sh1, sh2, sh3, sh4 = current_sh1[0][0], current_sh1[1][0], current_sh1[2][0], current_sh1[3][0]

    # проверим, что расписаний сколько нужно создалось
    # print(current_sh1)
    assert len(current_sh1) == 4, "неверное колво current_sh1"

    # проверим удаление, удалим второе расписание
    my_db.remove_schedule(sh2)
    current_sh2 = my_db.get_schedule(telegram_chat_id=1111111)
    print(current_sh2)
    assert len(current_sh2) == 3, "неверное колво current_sh2"
    assert current_sh2 == [current_sh1[0]] + current_sh1[2:], \
        "неверное содержание current_sh2"

    m_sh1 = my_db.edit_schedule(schedule_id=sh1, new_weekday=2, new_sport=None, new_gym=g2, new_time=None)
    m_sh2 = my_db.edit_schedule(schedule_id=sh3, new_weekday=None, new_sport="Non", new_gym=None, new_time="19.31")
    m_sh3 = my_db.edit_schedule(schedule_id=sh4, new_weekday=6, new_sport="Non", new_gym=g4, new_time="19.32")
    m_sh4 = my_db.edit_schedule(schedule_id=sh1, new_weekday=None, new_sport=None, new_gym=None, new_time=None)
    print(m_sh1, m_sh2, m_sh3, m_sh3, sep='\n')

    # TODO добавить assert на содержание текущего набота расписание
    current_sh3 = my_db.get_schedule(telegram_chat_id=1111111)
    # print(m_sh1, m_sh2, m_sh3, m_sh4, sep='\n')
    # print(current_sh3)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test_new_chat())
    loop.close()
