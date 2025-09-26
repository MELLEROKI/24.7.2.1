Михаил️️️️️️️️, [26.09.2025 17:20]
import requests
import json

class PetFriendsAPI:
    def __init__(self):
        self.base_url = "https://petfriends.skillfactory.ru/"
        self.api_key = None

    def get_api_key(self, email: str, password: str) -> tuple:
        """Получение API ключа"""
        headers = {
            'email': email,
            'password': password
        }
        response = requests.get(self.base_url + 'api/key', headers=headers)
        status = response.status_code
        result = ""
        try:
            result = response.json()
            if status == 200:
                self.api_key = result['key']
        except json.decoder.JSONDecodeError:
            result = response.text
        return status, result

    def get_list_of_pets(self, filter: str = "") -> tuple:
        """Получение списка питомцев"""
        headers = {'auth_key': self.api_key}
        filter = {'filter': filter}
        response = requests.get(self.base_url + 'api/pets', headers=headers, params=filter)
        status = response.status_code
        result = ""
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text
        return status, result

    def add_new_pet(self, name: str, animal_type: str, age: str, pet_photo: str) -> tuple:
        """Добавление нового питомца с фото"""
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age,
        }
        files = {'pet_photo': open(pet_photo, 'rb')}
        headers = {'auth_key': self.api_key}
        response = requests.post(self.base_url + 'api/pets', headers=headers, data=data, files=files)
        status = response.status_code
        result = ""
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text
        return status, result

    def delete_pet(self, pet_id: str) -> tuple:
        """Удаление питомца"""
        headers = {'auth_key': self.api_key}
        response = requests.delete(self.base_url + 'api/pets/' + pet_id, headers=headers)
        status = response.status_code
        result = ""
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text
        return status, result

    def update_pet_info(self, pet_id: str, name: str, animal_type: str, age: str) -> tuple:
        """Обновление информации о питомце"""
        headers = {'auth_key': self.api_key}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        response = requests.put(self.base_url + 'api/pets/' + pet_id, headers=headers, data=data)
        status = response.status_code
        result = ""
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text
        return status, result

    # Дополнительные методы, которые нужно реализовать
    def add_new_pet_simple(self, name: str, animal_type: str, age: str) -> tuple:
        """Добавление нового питомца без фото"""
        headers = {'auth_key': self.api_key}
        data = {
            'name': name,
            'animal_type': animal_type,
            'age': age
        }
        response = requests.post(self.base_url + 'api/create_pet_simple', headers=headers, data=data)
        status = response.status_code
        result = ""
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:
            result = response.text
        return status, result

    def set_pet_photo(self, pet_id: str, pet_photo: str) -> tuple:
        """Добавление фото питомца"""
        files = {'pet_photo': open(pet_photo, 'rb')}
        headers = {'auth_key': self.api_key}
        response = requests.post(self.base_url + 'api/pets/set_photo/' + pet_id, headers=headers, files=files)
        status = response.status_code
        result = ""
        try:
            result = response.json()
        except json.decoder.JSONDecodeError:

Михаил️️️️️️️️, [26.09.2025 17:20]
result = response.text
        return status, result
