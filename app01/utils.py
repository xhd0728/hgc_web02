import time
import random
import pymysql
import hashlib
from django.utils.safestring import mark_safe

# 传入时间戳


def get_date(stamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamp))

# 传入年月日时间分秒


def get_stamp(d):
    tp = time.strptime(d, '%Y-%m-%d %H:%M:%S')
    return int(time.mktime(tp))

# 获取一个永不重复的名字


def get_name(name=''):
    timer = str(time.time()).replace('.', '')
    rands = random.randint(10000, 99999)
    suf = '_' if name else ''
    return name + suf + timer + str(rands)

# 加密工具


def set_hash(sr):
    md5 = hashlib.md5()
    md5.update(sr.encode('utf-8'))
    return md5.hexdigest()


# 思想：调用的时候往里传数据
# 思想：调用一次DB类，就断开一次连接
class DB:
    # 构造
    def __init__(
            self,
            host,
            user,
            passwd,
            db,
            port=3306,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
    ):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port
        self.charset = charset
        self.cursorclass = cursorclass

    # 创建连接
    def __conn(self):
        # 实例属性
        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            passwd=self.passwd,
            db=self.db,
            port=self.port,
            charset=self.charset,
            cursorclass=self.cursorclass
        )
        return self.conn.cursor()  # 返回游标对象

    # 查询执行：无需提交
    def __query(self, sql):
        cursor = self.__conn()
        cursor.execute(sql)
        return cursor

    # 增删改执行
    def __execute(self, sql, flag=False):
        cursor = self.__conn()
        row = cursor.execute(sql)       # 影响行数
        self.conn.commit()              # 提交
        if flag:
            return cursor.lastrowid     # 新增行数
        return row                      # 默认返回影响行数

    # 增
    def insert(self, sql):
        return self.__execute(sql, flag=True)

    # 删
    def delete(self, sql):
        return self.__execute(sql)

    # 改
    def update(self, sql):
        return self.__execute(sql)

    # 查
    def findall(self, sql):
        return self.__query(sql).fetchall()

    def findone(self, sql):
        return self.__query(sql).fetchone()

    # 析构
    def __del__(self):
        self.__conn().close()       # 释放游标
        self.conn.close()           # 释放连接


# 分页处理
# 参数1：当前页数
# 参数2：总条数
# 参数3：每页显示条数
def handle_page(page, total_count, page_size, **dt):

    # 参数处理
    args = ''
    for key, value in dt.items():
        args += '&'+str(key)+'='+str(value)

    total_page_count, div = divmod(total_count, page_size)
    if div:
        total_page_count += 1

    # 极值页码处理
    plus = 5
    if total_page_count <= 2 * plus + 1:
        start_page = 1
        end_page = total_page_count
    else:
        if page <= plus:
            start_page = 1
            end_page = 2 * plus + 1
        else:
            if (page + plus) > total_page_count:
                start_page = total_page_count - 2 * plus
                end_page = total_page_count
            else:
                start_page = page - plus
                end_page = page + plus

    page_str_list = []

    # 首页
    page_str_list.append('<li><a href="?page=1'+args+'">首页</a></li>')

    # 上一页
    if page > 1:
        prev = '<li><a href="?page=' + \
            str(page-1)+args + \
            '" aria-label="Previous"><span aria-hidden="true">上一页</span></a></li>'
    else:
        prev = '<li><a href="?page=1'+args + \
            '" aria-label="Previous"><span aria-hidden="true">上一页</span></a></li>'
    page_str_list.append(prev)

    # 页码
    for i in range(start_page, end_page + 1):
        if i == page:
            ele = '<li class="active" style="background-color:#086C9D;"><a href="?page=' + \
                str(i)+args+'" style="color:white;">'+str(i)+'</a></li>'
        else:
            ele = '<li><a href="?page='+str(i)+args+'">'+str(i)+'</a></li>'
        page_str_list.append(ele)

    # 下一页
    if page < total_page_count:
        nt = '<li><a href="?page=' + \
            str(page+1)+args + \
            '" aria-label="Previous"><span aria-hidden="true">下一页</span></a></li>'
    else:
        nt = '<li><a href="?page=' + \
            str(total_page_count)+args + \
            '" aria-label="Previous"><span aria-hidden="true">下一页</span></a></li>'
    page_str_list.append(nt)

    # 尾页
    page_str_list.append('<li><a href="?page=' +
                         str(total_page_count)+args+'">尾页</a></li>')
    page_string = mark_safe(''.join(page_str_list))
    return page_string
