from db_class import DB
from env import DB_PATH

my_db = DB(DB_PATH)

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

m_sh1 = my_db.edit_schedule(schedule_id=sh1, weekday=2, sport=None, gym=g2, time=None)
m_sh2 = my_db.edit_schedule(schedule_id=sh3, weekday=None, sport="Non", gym=None, time="19.31")
m_sh3 = my_db.edit_schedule(schedule_id=sh4, weekday=6, sport="Non", gym=g4, time="19.32")
m_sh4 = my_db.edit_schedule(schedule_id=sh1, weekday=None, sport=None, gym=None, time=None)
print(m_sh1, m_sh2, m_sh3, m_sh3, sep='\n')

# TODO добавить assert на содержание текущего набота расписание
current_sh3 = my_db.get_schedule(telegram_chat_id=1111111)
# print(m_sh1, m_sh2, m_sh3, m_sh4, sep='\n')
# print(current_sh3)
