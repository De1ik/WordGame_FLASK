from user_db import UseDb


class UpdateStats:
    def __init__(self, db_config, user_id):
        self._config = db_config
        self._user_id = user_id
        self.sql = """UPDATE statistics 
                SET
                {stats} = {stats} + 1
                WHERE user_id = {user_id}"""
        
    def upd_tmplt(self, stats=None, sql=None, attempts=None):
        if not sql:
            sql = self.sql
        with UseDb(self._config) as cursor:
            cursor.execute(sql.format(stats=stats, user_id=self._user_id, attempts=attempts))

    def total_guessed(self):
        self.upd_tmplt('total_guessed')

    def total_attempt(self):
        self.upd_tmplt('total_attempt')
    
    def attempt_number(self, attempts):
        if attempts == 1:
            self.upd_tmplt('first_try') #'first_try'
        elif attempts <= 3:
            self.upd_tmplt('third_try') #'third_try'

    def max_attempt(self, attempts):
        sql = """UPDATE statistics 
                SET
                {stats} = {attempts}
                WHERE user_id = {user_id} and {stats} < {attempts}"""
        self.upd_tmplt('max_attempt', sql, attempts)

    def average_attempt(self):
        sql = """UPDATE statistics
                SET average_attempt = 
                    CASE 
                        WHEN total_guessed > 0 and total_attempt > 0 THEN total_attempt / total_guessed
                        ELSE 0 
                END
                WHERE user_id = {user_id}"""
        self.upd_tmplt(sql=sql)
        print('AVERAGE ATTEMPT')

        