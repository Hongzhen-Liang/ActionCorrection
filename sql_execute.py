import pymysql
import hashlib
user='root'
password='密码'
database='sEmg'

# 密码函数
def MD5(str):
    hash1 = hashlib.md5(bytes('sinscry',encoding='utf-8'))  # 加密参数(sinscry密钥)
    hash1.update(str.encode(encoding='utf-8'))
    return hash1.hexdigest()

def sql_insert(id1, psw):
    conn = pymysql.connect(host='127.0.0.1', user=user, password=password, database=database, charset='utf8')
    # 得到一个可以执行SQL语句的光标对象
    cursor = conn.cursor()
    # 定义要执行的SQL语句
    sql = "insert into users(id,psw) values(%s,%s);"
    # result=cursor.execute(sql,[id1,type1,price,submission_date])
    try:
        result = cursor.execute(sql, [id1, psw])
        # 涉及写操作要注意提交
        conn.commit()
    except pymysql.err.IntegrityError:
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return True
    # 关闭光标对象
    cursor.close()
    # 关闭数据库连接
    conn.close()
    return False


def sql_login(id):
    conn = pymysql.connect(host='127.0.0.1', user=user, password=password, database=database, charset='utf8')
    cursor = conn.cursor()
    sql = "select psw from users where id = %s"
    message = ''
    status = False
    try:
        result=cursor.execute(sql, [id])
        # 涉及写操作要注意提交
        conn.commit()
        message = cursor.fetchall()[0][0]
        status = True
    finally:
        print(message)
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return status, message

def sql_integral(id):
    conn = pymysql.connect(host='127.0.0.1', user=user, password=password, database=database, charset='utf8')
    cursor = conn.cursor()
    sql = "select integral from users where id = %s"
    message = ''
    try:
        result=cursor.execute(sql, [id])
        # 涉及写操作要注意提交
        conn.commit()
        message = cursor.fetchall()[0][0]
    finally:
        print(message)
        cursor.close()
        # 关闭数据库连接
        conn.close()
        return message


 