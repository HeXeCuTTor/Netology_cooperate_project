import vk_api, json 
from vk_api.longpoll import VkLongPoll, VkEventType
from DB_code import print_man, print_photos, add_to_selected, print_selected_list, fill_DB
from VK_download import VK
from config import token_VK, token

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


class User(): # этот класс, если пользователь повторяется

    def __init__(self, id, mode):
        self.id = id
        self.mode = mode


def get_keyboard(buts): # функция создания клавиатур
    nb = []
    for i in range(len(buts)):
        nb.append([])
        for k in range(len(buts[i])):
            nb[i].append(None)
    for i in range(len(buts)):
        for k in range(len(buts[i])):
            text = buts[i][k][0]
            color = {'зеленый' : 'positive',  'красный' : 'negative', 'синий' : 'primary'}[buts[i][k][1]]
            nb[i][k] = {"action": {"type": "text", "payload": "{\"button\": \"" + "1" + "\"}", "label": f"{text}"}, "color": f"{color}"}
    first_keyboard = {'one_time': False, 'buttons': nb}
    first_keyboard = json.dumps(first_keyboard, ensure_ascii=False).encode('utf-8')
    first_keyboard = str(first_keyboard.decode('utf-8'))
    return first_keyboard


start_key = get_keyboard([
    [('Выбрать параметры', 'синий'), ('Результаты поиска', 'зеленый')] # сами клавиатуры
]) 


search_key = get_keyboard([
    [('Добавить в избранные', 'красный'), ('Следущий пользователь', 'зеленый')],
    [('Избранные', 'синий')]
])


def sender(id, text, key):
    vk.method('messages.send', {'user_id' : id, 'message': text,  'random_id': 0, 'keyboard': key})    


users = []
man_id = 0
# бот
for event in longpoll.listen():
    if event.type == VkEventType.MESSAGE_NEW and event.to_me:
        
            request = event.text
            id = event.user_id
            msg = event.text.lower()

            if msg == 'начать':
                flag1 = 0
                for user in users:
                    if user.id == id:
                        sender(id, 'Выберите команду: ', start_key)
                        user.mode = 'start'
                        flag1 = 1
                if flag1 == 0:
                    users.append(User(id, 'start'))
                    sender(id, 'Приветствую! Это бот VkTinder. Бот создан для знакомства с людьми по всему миру! \U0001F604 \nВыберите действие: ', start_key)


            for user in users:
                if user.id == id:

                    if user.mode == 'start':
                        if msg == 'выбрать параметры':
                            sender(id, 'Введите следующие пареметры через запятую: страна, регион, город, пол, возраст от, возраст до. Пример: Россия, Московская область, Москва, М, 18, 30', start_key)
                            for event in longpoll.listen():
                                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                    xxx = event.text
                                    search_param = xxx.split(',')
                                    if len(search_param) == 6:
                                        country = search_param[0].strip()
                                        region = search_param[1].strip()
                                        city = search_param[2].strip()
                                        sex = search_param[3].strip()
                                        age_from = search_param[4].strip()
                                        age_to = search_param[5].strip()
                                        sender(id, 'Ожидайте, идёт поиск...', start_key)
                                        vk1 = VK(token_VK)
                                        get_country = vk1.get_id_countries(search_param[0])
                                        get_city = vk1.get_id_city(get_country, region, city)
                                        get_search_free = vk1.users_get_free(sex, age_from, age_to, get_city)
                                        fill_DB()
                                        sender(id, 'Данные сформированы, перейдите в "Результаты поиска"', start_key)
                                        break
                                    else:
                                        sender(id, 'Неправильный формат данных, нажмите на кнопку "Выбрать параметры" и введите корректные данные', start_key)
                                        break
                           
                        if msg == 'результаты поиска':
                            sender(id, 'Для просмотра нажмите кнопку "Следущий пользователь"', search_key)
                            user.mode = 'search'

                    if user.mode == 'search':
                        if msg == 'добавить в избранные':
                            add_to_selected(man_id)
                            sender(id, 'Пользователь добавлен в Избранное', search_key)

                        if msg == 'следущий пользователь':
                            man_id += 1
                            line = print_man(man_id)
                            if line is None:
                                sender(id, 'Список закончен', search_key)
                            else:
                                sender(id, f'{line[0]} {line[1]}\n{line[2]}', search_key)
                                x = print_photos(line[2])
                                for i in x:
                                    vk.method("messages.send",
                                            {"user_id": id, "message": "foto", "attachment": i[0], "random_id": 0,
                                            'keyboard': search_key})
                                break

                        if msg == 'избранные':
                            y = print_selected_list()
                            for i in y:
                                sender(id, f'{i[0]} {i[1]}\n{i[2]}', search_key)

