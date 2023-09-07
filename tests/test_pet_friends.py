from RestFUL_autotests_SF.api import PetFriends
from RestFUL_autotests_SF.settings import valid_email, valid_password, not_valid_email, not_valid_password
import os

pf = PetFriends()


def test_successful_add_new_pet_without_photo(name='Бибик', animal_type='каменьтерьер',
                                              age='6'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_successful_add_pet_photo(pet_photo='images/cat2.jpg'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    image = os.path.join(os.path.dirname(__file__), pet_photo)
    pet_id = my_pets['pets'][0]['id']
    if len(my_pets['pets']) > 0:
        status, result = pf.add_pet_photo(auth_key, pet_id, image)
        assert status == 200
    else:
        raise Exception("Мои питомцы отсутствуют!")


def test_get_apikey_with_invalid_userdata(email=not_valid_email, password=not_valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    print("Вы ввели неверный email и пароль!")


def test_delete_pet_with_invalid_auth_key():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    invlid_auth_key = {"key": "e29addb617116dfd656a96f40aed887a4fc371acb748f7637686a25"}
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Мурзик", "кот", "2", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(invlid_auth_key, pet_id)
    assert status == 403
    print("Неверный ключ авторизации!")


def test_get_my_pets(filter='my_pets'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    if len(result['pets']) > 0:
        assert status == 200
    else:
        raise Exception("Мои питомцы отсутствуют!")


def test_create_pet_with_invalid_data(name='', animal_type='', age=''):
    '''При отправке запроса возращает статус с кодом 200, создает
    питомца с пустыми ячейками'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400
    print('Введены невалидные данные')


def test_update_pet_info_with_invalid_data(name='', animal_type='', age=''):
    '''При отправке запроса возращает статус с кодом 200, успешно
    обновляет данные питомца, так как допускается ввод пустых значений'''
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 400
        print('Введены невалидные данные питомцев')


def test_update_pet_with_invalid_auth_key(name='Лариса', animal_type='мышь', age='1'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    invlid_auth_key = {"key": "e29addb617116dfd656a96f40aed887a4fc371acb748f7637686a25"}
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(invlid_auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 403
        print('Не верный ключ авторизации')
    else:
        raise Exception('Мои питомцы отсутствуют')


def test_get_list_of_pets_with_invalid_auth_key(filter=''):
    invlid_auth_key = {"key": "e29addb617116dfd656a96f40aed887a4fc371acb748f7637686a25"}
    status, result = pf.get_list_of_pets(invlid_auth_key, filter)
    assert status == 403
    print('Неверный ключ авторизации')


def test_get_api_key_with_no_valid_password(email=valid_email, password=not_valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result
    print("Введен неверный пароль!")

