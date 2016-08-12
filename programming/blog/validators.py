import re
import requests
from django.conf import settings
from django.forms import ValidationError
from django.utils.deconstruct import deconstructible
import xmltodict


@deconstructible
class MinLengthValidator(object):
    def __init__(self, min_length):
        self.min_length = min_length

    def __call__(self, value):
        if len(value) < self.min_length:
            raise ValidationError('{}글자 이상 입력해주세요.'.format(self.min_length))


@deconstructible
class ZipCodeValidator(object):
    '우편번호 체계안내 : http://www.koreapost.go.kr/kpost/sub/subpage.jsp?contId=010101040100'

    def __init__(self, is_check_exist =False):
        self.is_check_exist = is_check_exist

    def __call__(self, zip_code):
        if not re.match(r'^\d{5,6}$', zip_code):
            raise ValidationError('5자리 혹은 6자리 숫자로 입력해주세요.')

        if self.is_check_exist:
            self.check_exist_from_db(zip_code)

    def check_exist_from_db(self, zip_code):
        from blog.models import ZipCode
        if not ZipCode.objects.filter(code=zip_code).exists():
            raise ValidationError('없는 우편번호입니다.')

    def check_exist(self, zip_code):
        '우체국 open api : http://biz.epost.go.kr/customCenter/custom/custom_10.jsp'

        params = {
            'regkey': settings.EPOST_API_KEY,
            'target': 'postNew',
            'query': zip_code,
        }
        xml = requests.get('http://biz.epost.go.kr/KpostPortal/openapi', params=params).text
        response = xmltodict.parse(xml)
        try:
            error = response['error']
        except KeyError:
            pass
        else:
            raise ValidationError('[{error_code}] {message}'.format(**error))


'''
def min_length_validator(min_length):
    def wrap(value):
        if len(value) < min_length:
            raise ValidationError('{}글자 이상 입력해주세요.'.format(min_length))
    return wrap


def max_length_validator(max_length):
    def wrap(value):
        if len(value) > max_length:
            raise ValidationError('{}글자 이하 입력해주세요.'.format(max_length))
    return wrap
'''


def lnglat_validator(value):
    if not re.match(r'^(\d+\.?\d*),(\d+\.?\d*)$', value):
        raise ValidationError('Invalid LngLat Type')


def phone_number_validator(value):
    if not re.match(r'^01[06789][1-9]\d{6,7}$', value):
        raise ValidationError('휴대폰 번호를 입력해주세요.')

