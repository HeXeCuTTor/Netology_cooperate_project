import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from DB_code import add_to_selected, print_selected_list, fill_user_info, fill_params, fill_photo_info
from VK_download import VK
from config import token_VK, token

vk = vk_api.VkApi(token=token)
longpoll = VkLongPoll(vk)


class User():  # этот класс, если пользователь повторяется

    def __init__(self, id, mode):
        self.id = id
        self.mode = mode


def get_keyboard(buts): # функция создания клавиатур
    nb = []
    for index in range(len(buts)):
        nb.append([])
        for key in range(len(buts[index])):
            nb[index].append(None)
            text = buts[index][key][0]
            color = {'зеленый' : 'positive',  'красный' : 'negative', 'синий' : 'primary'}[buts[index][key][1]]
            nb[index][key] = {"action": {"type": "text", "payload": "{\"button\": \"" + "1" + "\"}", "label": f"{text}"}, "color": f"{color}"}
    first_keyboard = {'one_time': False, 'buttons': nb}
    first_keyboard = json.dumps(first_keyboard, ensure_ascii=False).encode('utf-8')
    first_keyboard = str(first_keyboard.decode('utf-8'))
    return first_keyboard


start_key = get_keyboard([
    [('Выбрать параметры', 'синий'), ('Результаты поиска', 'зеленый')]  # сами клавиатуры
]) 


search_key = get_keyboard([
    [('Добавить в избранные', 'красный'), ('Следущий пользователь', 'зеленый')],
    [('Избранные', 'синий')]
])


def sender(id, text, key):
    vk.method('messages.send', {'user_id': id, 'message': text,  'random_id': 0, 'keyboard': key})


users = []
index = -1
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
                    sender(id, 'Выберете команду: ', start_key)
                    user.mode = 'start'
                    flag1 = 1
            if flag1 == 0:
                users.append(User(id, 'start'))
                sender(id, 'Приветствую! Это бот VkTinder. Бот создан для знакомства с людьми по всему миру! \U0001F604 \nВыберите действие: ', start_key)

        for user in users:
            if user.id == id:

                if user.mode == 'start':
                    if msg == 'выбрать параметры':
                        sender(id, 'Введите следующие параметры через запятую: страна, регион, город, пол, возраст от, возраст до. Пример:Россия, Московская область, Москва, М, 18, 30.', start_key)
                        for event in longpoll.listen():
                            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                                xxx = event.text
                                search_param = xxx.split(',')
                                if len(search_param) == 6:
                                    printed = 'Данные сформированы, перейдите в "Результаты поиска"'
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
                                    search_id = fill_params(country, region, city, sex, age_from, age_to)
                                    sender(id, 'Данные сформированы, перейдите в "Результаты поиска"', start_key)
                                    break
                                else:
                                    sender(id, 'Неправильный формат данных, нажмите на кнопку "Выбрать параметры" и введите корректные данные', start_key)
                                    break

                    if msg == 'результаты поиска':
                        sender(id, 'Для просмотра нажмите кнопку "Следущий пользователь"', search_key)
                        user.mode = 'search'

                if user.mode == 'search':
                    if msg == 'следущий пользователь':
                        index += 1
                        if index == len(get_search_free):
                            sender(id, 'Список закончен', search_key)
                        else:
                            line = get_search_free[index]
                            sender(id,
                                    f"{line.get('first_name')} {line.get('last_name')}\nhttps://vk.com/id{line.get('user_id')}",
                                    search_key)
                            id_u = fill_user_info(line.get('first_name'), line.get('last_name'), f"https://vk.com/id{line.get('user_id')}", search_id)
                            users_photos_id = 0
                            while users_photos_id != (len(line) - 3):
                                users_photos_id += 1
                                vk.method("messages.send",
                                            {"user_id": id, "message": "foto",
                                            "attachment": f"photo{line.get('user_id')}_{line.get(f'photo_id {users_photos_id}')}",
                                            "random_id": 0,
                                            'keyboard': search_key})
                                fill_photo_info(f"photo{line.get('user_id')}_{line.get(f'photo_id {users_photos_id}')}", id_u)

                    if msg == 'добавить в избранные':
                        add_to_selected(id_u)
                        sender(id, 'Пользователь добавлен в Избранное', search_key)

                    if msg == 'избранные':
                        selected = print_selected_list(search_id)
                        for man in selected:
                            sender(id, f'{man[0]} {man[1]}\n{man[2]}', search_key)