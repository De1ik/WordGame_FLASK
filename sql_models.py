from user_db import UseDb
from werkzeug.security import generate_password_hash, check_password_hash

def email_db_check(db_config, email):
    with UseDb(db_config) as cursor:
        SQL = """SELECT count(*) FROM user_info WHERE email = %s"""
        cursor.execute(SQL, [email])
        res = cursor.fetchall()
        email_db = res[0][0]
        if email_db > 0:
            return True
        return False


def sign_up_page(db_config, name, email, password):
    try:
        with UseDb(db_config) as cursor:
            SQL = """INSERT INTO user_info
                    (name, email, password)
                    VALUES
                    (%s, %s, %s)"""
            cursor.execute(SQL, (name, email, password))
            id_sql = 'SELECT user_id FROM user_info WHERE email LIKE %s'
            cursor.execute(id_sql, [email])
            res = cursor.fetchall()
            user_id = res[0][0]
            return user_id
    except Exception as ex:
        print(ex)
        return False
    

def login_page(db_config, email, password):
    try:
        with UseDb(db_config) as cursor:
            data_checking_sql = 'SELECT user_id, password, count(email) as checking FROM user_info WHERE email = %s'
            cursor.execute(data_checking_sql, [email])
            result = cursor.fetchall()[0]
            if result[0]:
                user_id, db_password, email_count = result
                if email_count>0 and check_password_hash(db_password, password):
                    return user_id
    except Exception as ex:
        print(ex)
        return False


def review_page(db_config, user_id, review):
    try:
        with UseDb(db_config) as cursor:
            SQL = """INSERT INTO reviews
                    (user_id, review)
                    VALUES
                    (%s, %s)"""
            cursor.execute(SQL, (user_id, review))
            return True
    except Exception as ex:
        print(ex)
        return False


def profile_get_stats(db_config, user_id):
    try:
        with UseDb(db_config) as cursor:
            SQL = """SELECT total_guessed, total_attempt, first_try, third_try, average_attempt, max_attempt 
                     FROM statistics 
                     WHERE user_id = %s"""
            cursor.execute(SQL, [user_id])
            stats = cursor.fetchall()[0]
            print(f'STATS: {stats}')
            return stats
    except Exception as ex:
        print(ex)
        return False
    

def profile_persdata(db_config, user_id):
    try:
        with UseDb(db_config) as cursor:
            SQL = """SELECT name, email
                     FROM user_info 
                     WHERE user_id = %s"""
            cursor.execute(SQL, [user_id])
            persdata = cursor.fetchall()[0]
            print(f'PERSDATA: {persdata}')
            return persdata
    except Exception as ex:
        print(ex)
        return False
    