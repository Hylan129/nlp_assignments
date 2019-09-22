import pymysql,pandas

config ={
    'host':"rm-8vbwj6507z6465505ro.mysql.zhangbei.rds.aliyuncs.com",
    'port':3306,
    'user':'root',
    'password':'AI@2019@ai',
    'db':'stu_db',
    'charset':'utf8mb4',
    'cursorclass':pymysql.cursors.DictCursor,
}

con=pymysql.connect(**config)
try:
    with con.cursor() as cursor:
        sql = "select * from news_chinese"
        cursor.execute(sql)
        result = cursor.fetchall()
finally:
    con.close()
news_content = pandas.DataFrame(result).content
