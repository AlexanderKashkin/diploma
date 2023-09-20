import os

import allure
import pytest
from dotenv import load_dotenv

from api.resourses.contact import add_contact
from api.resourses.contact.contact_model import ContactModel
from api.resourses.user import UserModel
from api.resourses.user import auth
from utils import StatusCode
from utils.generator_random import generate_random_string


@pytest.fixture
def user_data_for_register():
    """
    The first and last name must be unique
    """
    first_name = f'Ivan_{generate_random_string(4)}'
    last_name = f'Ivanov_{generate_random_string(4)}'
    password = '1234567'
    return UserModel(first_name=first_name, last_name=last_name, password=password)


@pytest.fixture(scope='session', autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope='session')
def get_user_data_from_env():
    with allure.step('Получаем данные по пользователю'):
        resp = auth(email=os.getenv('EMAIL'),
                    password=os.getenv('PASSWORD'))
        assert resp.status_code == StatusCode.OK
        return UserModel(token=resp.json()['token'], _id=resp.json()['user']['_id'])


@pytest.fixture()
def data_contact():
    contact = ContactModel()
    contact.first_name = 'Alexander'
    contact.last_name = 'Pushkin'
    contact.birthdate = '1799-06-06'
    contact.email = 'alexander_pushkin@gmail.com'
    contact.phone = '8005555555'
    contact.street1 = 'street Glinka'
    contact.street2 = 'house 5, flat 17'
    contact.city = 'Moscow'
    contact.state_province = 'RU'
    contact.postal_code = '12345'
    contact.country = 'Russia'
    return contact


@pytest.fixture()
def add_contact_fixture(get_user_data_from_env, data_contact):
    with allure.step('Создаём контакт'):
        return add_contact(get_user_data_from_env.token, data_contact)
