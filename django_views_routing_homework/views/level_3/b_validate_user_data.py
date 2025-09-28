"""
В этом задании вам нужно реализовать вьюху, которая валидирует данные о пользователе.

- получите json из тела запроса
- проверьте, что данные удовлетворяют нужным требованиям
- если удовлетворяют, то верните ответ со статусом 200 и телом `{"is_valid": true}`
- если нет, то верните ответ со статусом 200 и телом `{"is_valid": false}`
- если в теле запроса невалидный json, вернуть bad request

Условия, которым должны удовлетворять данные:
- есть поле full_name, в нём хранится строка от 5 до 256 символов
- есть поле email, в нём хранится строка, похожая на емейл
- есть поле registered_from, в нём одно из двух значений: website или mobile_app
- поле age необязательное: может быть, а может не быть. Если есть, то в нём хранится целое число
- других полей нет

Для тестирования рекомендую использовать Postman.
Когда будете писать код, не забывайте о читаемости, поддерживаемости и модульности.
"""

from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest, JsonResponse
import json
import re
from enum import Enum


class RegisteredFrom(Enum):
    WEB = 'website'
    MOBILE = 'mobile_app'


KNOWN_FIELDS = ['full_name', 'email', 'registered_from', 'age']


def validate_full_name(data: dict) -> bool:
    if 'full_name' not in data:
        return False

    if type(data['full_name']) is not type('str'):
        return False

    if len(data['full_name']) < 5 or len(data['full_name']) > 256:
        return False

    return True


def validate_email(data: dict) -> bool:
    if 'email' not in data:
        return False

    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'  # регулярку не я писала
    if re.match(regex, data['email']):
        return True

    return False


def validate_registered_from(data: dict) -> bool:
    if 'registered_from' not in data:
        return False

    return data['registered_from'] in [RegisteredFrom.WEB.value, RegisteredFrom.MOBILE.value]


def validate_age(data: dict) -> bool:
    if 'age' not in data:
        return True

    return type(data['age']) is type(1)


def validate_only_known_fields(data: dict) -> bool:
    for key in data.keys():
        if key not in KNOWN_FIELDS:
            return False

    return True


def validate_user_data_view(request: HttpRequest) -> HttpResponse:
    try:
        data = json.loads(request.body)
    except:
        return HttpResponseBadRequest()
    if all([
        validate_full_name(data),
        validate_email(data),
        validate_registered_from(data),
        validate_age(data),
        validate_only_known_fields(data)
    ]):
        return JsonResponse(data={"is_valid": True}, status=200)

    return JsonResponse(data={"is_valid": False}, status=200)
