from django.test import TestCase

# Create your tests here.
from app01.utils import DB
mysql = DB(host='127.0.0.1', user='root', passwd='10011010', db='hgx_web')
id_list = mysql.findall('select id from tab_lol')
for dt in id_list:
    id = dt['id']
    mysql.update(f'update tab_lol set num = "{id}" where id = "{id}"')
