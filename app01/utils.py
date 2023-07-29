import time
import random
import pymysql
import hashlib

# 传入时间戳
def get_date(stamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stamp))

# 传入年月日时间分秒
def get_stamp(d):
    tp = time.strptime(d, '%Y-%m-%d %H:%M:%S')
    return int(time.mktime(tp))

# 获取一个永不重复的名字
def get_name(name=''):
    timer = str(time.time()).replace('.','')
    rands = random.randint(10000, 99999)
    suf = '_' if name else ''
    return name + suf +timer + str(rands)

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
            host = self.host,
            user = self.user,
            passwd = self.passwd,
            db = self.db,
            port = self.port,
            charset = self.charset,
            cursorclass = self.cursorclass
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






