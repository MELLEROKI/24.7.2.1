Михаил️️️️️️️️, [26.09.2025 17:22]
import pytest
import os
from api.api import PetFriendsAPI

class TestPetFriendsAPI:
    def setup_method(self):
        self.pf = PetFriendsAPI()
        # Получаем API ключ перед каждым тестом
        self.valid_email = "valid_email@example.com"
        self.valid_password = "valid_password"
        self.pf.get_api_key(self.valid_email, self.valid_password)

    # 1. Позитивный тест - получение списка питомцев
    def test_get_all_pets_with_valid_key(self):
        """Тест получения списка всех питомцев с валидным ключом"""
        status, result = self.pf.get_list_of_pets()
        assert status == 200
        assert len(result['pets']) > 0

    # 2. Негативный тест - неверный email при получении ключа
    def test_get_api_key_with_invalid_email(self):
        """Тест получения API ключа с неверным email"""
        pf = PetFriendsAPI()
        status, result = pf.get_api_key("invalid_email", self.valid_password)
        assert status == 403  # Ожидаем статус "Запрещено"

    # 3. Негативный тест - неверный пароль при получении ключа
    def test_get_api_key_with_invalid_password(self):
        """Тест получения API ключа с неверным паролем"""
        pf = PetFriendsAPI()
        status, result = pf.get_api_key(self.valid_email, "invalid_password")
        assert status == 403

    # 4. Негативный тест - пустые credentials
    def test_get_api_key_with_empty_credentials(self):
        """Тест получения API ключа с пустыми данными"""
        pf = PetFriendsAPI()
        status, result = pf.get_api_key("", "")
        assert status == 403

    # 5. Граничный тест - добавление питомца с максимально длинным именем
    def test_add_pet_with_long_name(self):
        """Тест добавления питомца с очень длинным именем"""
        long_name = "A" * 1000  # Очень длинное имя
        status, result = self.pf.add_new_pet_simple(long_name, "dog", "5")
        assert status == 200
        assert result['name'] == long_name

    # 6. Негативный тест - добавление питомца с отрицательным возрастом
    def test_add_pet_with_negative_age(self):
        """Тест добавления питомца с отрицательным возрастом"""
        status, result = self.pf.add_new_pet_simple("Барсик", "кот", "-5")
        # Система может либо отклонить запрос, либо принять - зависит от реализации
        assert status in [200, 400]

    # 7. Негативный тест - добавление питомца с пустыми полями
    def test_add_pet_with_empty_fields(self):
        """Тест добавления питомца с пустыми обязательными полями"""
        status, result = self.pf.add_new_pet_simple("", "", "")
        assert status == 400  # Ожидаем "Неверный запрос"

    # 8. Негативный тест - обновление несуществующего питомца
    def test_update_nonexistent_pet(self):
        """Тест обновления информации о несуществующем питомце"""
        fake_pet_id = "nonexistent_pet_id_12345"
        status, result = self.pf.update_pet_info(fake_pet_id, "Новое имя", "собака", "3")
        assert status == 404  # Ожидаем "Не найдено"

    # 9. Негативный тест - удаление уже удаленного питомца
    def test_delete_already_deleted_pet(self):
        """Тест повторного удаления питомца"""
        # Сначала создаем питомца
        status, result = self.pf.add_new_pet_simple("Темп", "пес", "2")
        pet_id = result['id']
        
        # Удаляем его
        self.pf.delete_pet(pet_id)
        
        # Пытаемся удалить снова
        status, result = self.pf.delete_pet(pet_id)
        assert status == 404  # Ожидаем "Не найдено"

    # 10. Тест на SQL injection в поле имени
    def test_sql_injection_in_name_field(self):
        """Тест на уязвимость SQL injection в поле имени"""
        sql_injection_name = "'; DROP TABLE pets; --"
        status, result = self.pf.add_new_pet_simple(sql_injection_name, "кот", "3")
        # Система должна корректно обработать специальные символы
        assert status in [200, 400]
        if status == 200:
            assert result['name'] == sql_injection_name

    # 11. Тест с неверным форматом возраста (строка вместо числа)
    def test_add_pet_with_text_age(self):

Михаил️️️️️️️️, [26.09.2025 17:22]
"""Тест добавления питомца с текстом в поле возраста"""
        status, result = self.pf.add_new_pet_simple("Мурзик", "кот", "пять лет")
        assert status in [200, 400]

    # 12. Тест фильтрации питомцев с неверным фильтром
    def test_get_pets_with_invalid_filter(self):
        """Тест получения питомцев с неверным фильтром"""
        status, result = self.pf.get_list_of_pets("invalid_filter")
        # Система может вернуть пустой список или ошибку
        assert status in [200, 400]

    # 13. Тест добавления фото неверного формата
    def test_add_pet_with_invalid_photo_format(self):
        """Тест добавления питомца с фото неверного формата"""
        # Создаем временный файл с неверным форматом
        with open('invalid_photo.txt', 'w') as f:
            f.write('This is not an image')
        
        status, result = self.pf.add_new_pet("Бобик", "собака", "4", "invalid_photo.txt")
        os.remove('invalid_photo.txt')
        assert status == 400  # Ожидаем ошибку

    # 14. Тест с очень большим числом в возрасте
    def test_add_pet_with_very_large_age(self):
        """Тест добавления питомца с очень большим возрастом"""
        status, result = self.pf.add_new_pet_simple("Долгожитель", "черепаха", "9999")
        assert status in [200, 400]

    # 15. Тест с специальными символами в полях
    def test_add_pet_with_special_characters(self):
        """Тест добавления питомца со специальными символами"""
        name_with_specials = "Барсик!@#$%^&*()"
        animal_type_with_specials = "Кот-собакa混合"
        status, result = self.pf.add_new_pet_simple(name_with_specials, animal_type_with_specials, "3")
        assert status in [200, 400]
