import pymysql

def get_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user='root',
        password='0000',
        database='music_store',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False
    )
