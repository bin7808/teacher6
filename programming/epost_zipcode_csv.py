import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "programming.settings")
import django
django.setup()

import csv

CSV_PATH = '20150710_seoul.txt'

reader = csv.reader(open(CSV_PATH, 'rt', encoding='cp949'), delimiter='|')

from blog.models import ZipCode

columns = next(reader)

zip_code_list = []

for idx, row in enumerate(reader):
    data = dict(zip(columns, row))
    zip_code = ZipCode(
        city=data['시도'], road=data['도로명'], dong=data['법정동명'],
        gu=data['시군구'], code=data['우편번호'])
    zip_code_list.append(zip_code)
    # zip_code.save()

    # print(data['우편번호'])
    # if idx > 10: break

print('zip_code size : {}'.format(len(zip_code_list)))
ZipCode.objects.bulk_create(zip_code_list, 100)

