import sqlite3


class Database(object):
    """Database class offers some methods to operate the dota2 database."""

    # initialization: connect to sqlite3 db_file
    def __init__(self, db_file="dota2.db"):
        super(Database, self).__init__()
        self.db_file = db_file
        self.conn = sqlite3.connect(self.db_file)
        self.c = self.conn.cursor()
        return

    # delete Database object
    def __del__(self):
        self.close_db()
        return

    # close database connection
    def close_db(self):
        self.conn.close()
        return

    # commit sql
    def commit_sql(self):
        self.conn.commit()
        return

    # delete all data in table
    def delete_data(self, table):
        sql = "DELETE FROM {};".format(table)
        self.c.execute(sql)
        self.conn.commit()
        return

    # insert data into table heroes
    def insert_into_heroes(self, hero_name_en, hero_name_zh, hero_win_rate, hero_pic_url):
        sql = "INSERT INTO heroes (hero_name_en, hero_name_zh, hero_win_rate, hero_pic_url) \
    		VALUES ('{}', '{}', {}, '{}');".format(hero_name_en, hero_name_zh, hero_win_rate, hero_pic_url)
        self.c.execute(sql)
        return

    # insert data into table hero_pos
    def insert_into_pos(self, hero_name, pos1, pos2, pos3, pos4, pos5):
        sql = "INSERT INTO hero_pos (hero_name, pos1, pos2, pos3, pos4, pos5) \
    		VALUES ('{}', {}, {}, {});".format(hero_name, pos1, pos2, pos3, pos4, pos5)
        self.c.execute(sql)
        return

    # insert data into table hero_anti
    def insert_into_anti(self, hero_name, hero_anti, anti_rate, win_rate):
        sql = "INSERT INTO hero_anti (hero_name, hero_anti, anti_rate, win_rate) \
    		VALUES ('{}', '{}', {}, {});".format(hero_name, hero_anti, anti_rate, win_rate)
        self.c.execute(sql)
        return

    # insert data into table hero_comb
    def insert_into_comb(self, hero_name, hero_comb, comb_rate, win_rate):
        sql = "INSERT INTO hero_comb (hero_name, hero_comb, comb_rate, win_rate) \
    		VALUES ('{}', '{}', {}, {});".format(hero_name, hero_comb, comb_rate, win_rate)
        self.c.execute(sql)
        return

    # get all params in table system
    def get_system_params(self):
        sql = "SELECT * FROM system;"
        res = self.c.execute(sql)
        d = dict()
        for row in res:
            d[row[0]] = row[1]
        return d

    # get param value in table system
    def get_system_param_value(self, param_key):
        sql = "SELECT value FROM system WHERE key='{}';".format(param_key)
        res = self.c.execute(sql)
        if not res:
            return None
        return res[0][0]

    # set param value in table system
    def set_system_param_value(self, param_key, param_value):
        sql = "SELECT * FROM system WHERE key={}".format(param_key)
        res = self.c.execute(sql)
        if not res:
            sql = "INSERT INTO system (key, value) VALUES ('{}', '{}');".format(param_key, param_value)
        else:
            sql = "UPDATE system SET value='{}' WHERE key='{}';".format(param_value, param_key)
        self.c.execute(sql)
        return

    # get all hero names
    def get_hero_names(self):
        sql = "SELECT hero_name_en, hero_name_zh FROM heroes;"
        res = self.c.execute(sql)
        names = []
        for row in res:
            names.append((row[0], row[1]))
        return names

    # get hero en names
    def get_hero_names_en(self):
        sql = "SELECT hero_name_en FROM heroes;"
        res = self.c.execute(sql)
        names = []
        for row in res:
            names.append(row[0])
        return names

    # get hero zh names
    def get_hero_names_zh(self):
        sql = "SELECT hero_name_zh FROM heroes;"
        res = self.c.execute(sql)
        names = []
        for row in res:
            names.append(row[0])
        return names

    # get hero pic url by hero name
    def get_hero_pic(self, hero_name):
        sql = "SELECT hero_pic_url FROM heroes WHERE hero_name_zh='{}';".format(hero_name)
        res = self.c.execute(sql)
        return res[0][0]

    # get hero anti info by hero name
    def get_hero_anti(self, hero_name):
        sql = "SELECT hero_name, anti_rate, win_rate FROM hero_anti WHERE hero_anti='{}';".format(hero_name)
        res = self.c.execute(sql)
        return res

    # get hero comb info by hero name
    def get_hero_comb(self, hero_name):
        sql = "SELECT hero_name, comb_rate, win_rate FROM hero_comb WHERE hero_comb='{}';".format(hero_name)
        res = self.c.execute(sql)
        return res
