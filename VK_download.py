import requests
import json
from pprint import pprint
from config import token_VK

class VK:
    def __init__(self, token_VK,version='5.131'):
        self.token = token_VK
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def get_id_countries(self,country):
        self.country = country
        with open ('ISO 3166-1 alpha-2.txt', 'r', encoding = 'utf8') as file:
            content = file.readlines()
        for countries in content:
            if self.country in countries:
                identificator = countries[0:2]
                break
        url = 'https://api.vk.com/method/database.getCountries'
        params = {'code': identificator}
        response = requests.get(url, params={**self.params, **params}).json()
        for item in response.values():
            for keys,values in item.items():
                if keys == 'items':
                    for keys,values in values[0].items():
                        if keys == 'id':
                            id = values
        return id

    def get_id_city(self, get_country, region, city):
        self.region = region
        self.city = city
        self.country_id = get_country
        url = 'https://api.vk.com/method/database.getCities'
        params = {'country_id': self.country_id, 'q':self.city, 'need_all': 1}
        response = requests.get(url, params={**self.params, **params}).json()
        for item in response.values():
            for keys,values in item.items():
                if keys == 'items':
                    for diction in values:
                        for keys,value in diction.items():
                            if keys == 'id':
                                city_id = value
                            if value == self.region:
                                return city_id
                                
    def users_get_photo(self,user_id):
        url = 'https://api.vk.com/method/photos.get'
        self.id = user_id
        params = {'owner_id': self.id, 'album_id': 'profile', 'photo_sizes': 0, 'extended': 1, 'rev': 1}
        response = requests.get(url, params={**self.params, **params})
        photos_data = response.json()
        photos_json = []
        photo_data = {}
        for items in photos_data.values():
            for keys,values in items.items():
                if keys == 'items':
                    for list in values:
                        for key, value in list.items():
                            if key == 'likes':
                                likes = value.get('count')
                            if key == 'sizes':
                                photo_data['url'] = value[-1].get('url')      
                        photo_data['likes'] = likes
                        photos_json.append(photo_data)
                        photo_data = {}
        sorted_photos_json = (sorted(photos_json, key=lambda d: d['likes']))[-3:]
        return sorted_photos_json

    def users_get_free(self, sex, age_from, age_to, get_city):
        self.sex = sex
        self.age_from = age_from
        self.age_to = age_to
        self.city_id = get_city
        url = 'https://api.vk.com/method/users.search'
        params_1 = {'sort': 1, 'sex':self.sex, 'count': 10, 'fields': ['bdate'], 'city_id':self.city_id,'has_photo': 1, 'status': 1, 'age_from': self.age_from, "age_to": self.age_to, 'can_access_closed': 1}
        response_1 = requests.get(url, params={**self.params, **params_1}).json()
        params_6 = {'sort': 1, 'sex':self.sex, 'count': 10, 'fields': ['city','bdate'], 'city_id':self.city_id,'has_photo': 1, 'status': 6, 'age_from': self.age_from, "age_to": self.age_to, 'can_access_closed': 1}
        response_6 = requests.get(url, params={**self.params, **params_6}).json()
        def free_profile(response):
            users_data = {}
            users_dates = []
            for item in response.values():
                for keys,values in item.items():
                    if keys == 'items':
                        for list in values:
                            for key, value in list.items():
                                if key == 'bdate':
                                    birthday = value
                                if key == 'first_name':
                                    name = value
                                if key == 'id':
                                    user_id = value
                                if key == 'last_name':
                                    surname = value
                                if key == 'can_access_closed':
                                    if value == False:
                                        continue
                                    else:
                                        users_data['first_name'] = name
                                        users_data['last_name'] = surname
                                        users_data['bdate'] = birthday
                                        users_data['link'] = f'https://vk.com/id{user_id}'
                                        photos = vk.users_get_photo(user_id)
                                        num = 0                                    
                                        if photos != []:
                                            for photo in photos:
                                                for keys, values in photo.items():
                                                    if keys == 'url':
                                                        num += 1
                                                        users_data[f'{keys} {num}'] = values
                                            users_dates.append(users_data)
                                            users_data = {}
            return users_dates
        with open ('database.json', 'w', encoding = 'utf8') as f:
            json.dump(free_profile(response_1) + free_profile(response_6), f, sort_keys=False, ensure_ascii = False, indent = 2)
        return print("Done")
    

if __name__ == '__main__':
    # country = "Россия"
    # region = "Новосибирская область"
    # city = "Новосибирск"
    # sex = '1'
    # age_from = '18'
    # age_to = '30'
    vk = VK(token_VK)
    get_country = vk.get_id_countries(country)
    get_city = vk.get_id_city(get_country, region, city)
    get_search_free = pprint(vk.users_get_free(sex, age_from, age_to, get_city))
