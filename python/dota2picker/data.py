import requests
import re
import time
import numpy as np
from database import Database


class Data(object):
    """Data class offer some data about heroes"""

    # initialization: connect to database
    def __init__(self, db_file="dota2.db"):
        super(Data, self).__init__()
        self.db = Database(db_file)
        self.params = self.get_url_param()
        return

    # get url param
    def get_url_param(self):
        d = self.db.get_system_params()
        params = dict()
        params['time'] = d['data_time']
        params['server'] = d['data_server']
        params['skills'] = d['data_skills']
        params['ladder'] = d['data_ladder']
        return params

    # get content by url
    def get_url_content(self, url, params=None):
        res = None
        if not params:
            res = requests.get(url)
        else:
            res = requests.get(url, params=params)
        return res.text

    # update table heroes
    def update_heroes_table(self):
        self.db.delete_data("heroes")
        url = "http://www.dotamax.com/hero/rate/"
        content = self.get_url_content(url, self.params)
        hero_name_en = re.findall(r'dota2/images/heroes/([\S]+)_hphover.png', content)
        hero_name_zh = re.findall(r'<span class="hero-name-list">([\S]+)</span>', content)
        hero_win_rate = re.findall(r'<div style="height: 10px">([\S]+)%<\/div>', content)
        # hero_win_rate = re.findall(r'class="segment segment-green" style="width:([\S]+)%;">', content)
        length = len(hero_name_en)
        print("==========共查到英雄{}个==========".format(length))
        for i in range(length):
            pic_url = "http://cdn.dota2.com/apps/dota2/images/heroes/{}_hphover.png".format(hero_name_en[i])
            self.db.insert_into_heroes(hero_name_en[i], hero_name_zh[i], float(hero_win_rate[i]), pic_url)
        self.db.commit_sql()
        return

    # update table hero_anti
    def update_hero_anti_table(self):
        print()
        print("==========开始更新对手数据==========")
        start_time = time.time()
        cnt = 0
        self.db.delete_data("hero_anti")
        hero_names = self.db.get_hero_names()
        # print(hero_names)
        for hero_name_en, hero_name_zh in hero_names:
            url = "http://www.dotamax.com/hero/detail/match_up_anti/{}/".format(hero_name_en)
            content = self.get_url_content(url, self.params)
            hero_anti = re.findall(r'<span class="hero-name-list">([\S]+)</span>', content)
            rate = re.findall(r'<div style="height: 10px">([\S]+)%<\/div>', content)
            # p1 = re.findall(r'class="segment segment-green" style="width:([\S]+)%;">', content)
            # p2 = re.findall(r'class="segment segment-red" style="width:([\S]+)%;">', content)
            # anti_rate = p1 + p2
            # win_rate = re.findall(r'class="segment segment-gold" style="width:([\S]+)%;">', content)
            win_rate = []
            anti_rate = []
            for i in range(len(rate)):
                if i % 2:
                    win_rate.append(rate[i])
                else:
                    anti_rate.append(rate[i])
            length = len(hero_anti)
            for i in range(length):
                # print(hero_name_zh, hero_anti[i], float(anti_rate[i]), float(win_rate[i]))
                self.db.insert_into_anti(hero_name_zh, hero_anti[i], float(anti_rate[i]), float(win_rate[i]))
                cnt += 1
            self.db.commit_sql()
            fill = (6 - len(hero_name_zh)) * 2
            print(hero_name_zh, ' ' * fill, length, url)
        print("更新所用时间: {}s, 共记录数据:{}条".format(time.time() - start_time, cnt))
        self.check("hero_anti")
        print("==========更新对手数据结束==========")
        return

    # update table hero_comb
    def update_hero_comb_table(self):
        print()
        print("==========开始更新队友数据==========")
        start_time = time.time()
        cnt = 0
        self.db.delete_data("hero_comb")
        hero_names = self.db.get_hero_names()
        # print(hero_names)
        for hero_name_en, hero_name_zh in hero_names:
            url = "http://www.dotamax.com/hero/detail/match_up_comb/{}/".format(hero_name_en)
            content = self.get_url_content(url, self.params)
            hero_comb = re.findall(r'<span class="hero-name-list">([\S]+)</span>', content)
            rate = re.findall(r'<div style="height: 10px">([\S]+)%<\/div>', content)
            # p1 = re.findall(r'class="segment segment-green" style="width:([\S]+)%;">', content)
            # p2 = re.findall(r'class="segment segment-red" style="width:([\S]+)%;">', content)
            # comb_rate = p1 + p2
            # win_rate = re.findall(r'class="segment segment-gold" style="width:([\S]+)%;">', content)
            win_rate = []
            comb_rate = []
            for i in range(len(rate)):
                if i % 2:
                    win_rate.append(rate[i])
                else:
                    comb_rate.append(rate[i])
            length = len(hero_comb)
            for i in range(length):
                # print(hero_name_zh, hero_comb[i], float(comb_rate[i]), float(win_rate[i]))
                self.db.insert_into_comb(hero_name_zh, hero_comb[i], float(comb_rate[i]), float(win_rate[i]))
                cnt += 1
            self.db.commit_sql()
            fill = (6 - len(hero_name_zh)) * 2
            print(hero_name_zh, ' ' * fill, length, url)
        print("更新所用时间: {}s, 共记录数据:{}条".format(time.time() - start_time, cnt))
        self.check("hero_comb")
        print("==========更新队友数据结束==========")
        return

    # check if where is data lost
    def check(self, table):
        hero_names = self.db.get_hero_names()
        print("==========开始进行数据检查==========")
        check_res = []
        for _, h1 in hero_names:
            for _, h2 in hero_names:
                if h1 != h2:
                    sql = "SELECT * FROM {} WHERE hero_name='{}' AND {}='{}'".format(table, h1, table, h2)
                    res = self.db.c.execute(sql)
                    lst = list(res)
                    if not lst:
                        check_res.append((h1, h2))
        length = len(check_res)
        if length > 0:
            print("缺失数据{}条：".format(length))
            for r in check_res:
                print(r)
        else:
            print("无缺失数据")
        print("============数据检查完毕============")
        return

    # get hero zh names
    def get_hero_names_zh(self):
        return self.db.get_hero_names_zh()

    # calculate rate by anti and comb heroes
    def calc(self, anti, comb, ban=[]):
        all_heroes = self.get_hero_names_zh()
        info = dict()
        for hero in all_heroes:
            if hero not in anti and hero not in comb and hero not in ban:
                info[hero] = dict()
                info[hero]['anti'] = dict()
                info[hero]['anti']['anti_rate'] = dict()
                info[hero]['anti']['win_rate'] = dict()
                info[hero]['comb'] = dict()
                info[hero]['comb']['comb_rate'] = dict()
                info[hero]['comb']['win_rate'] = dict()
        for hero in anti:
            sql = "SELECT * FROM hero_anti WHERE hero_anti='{}';".format(hero)
            res = self.db.c.execute(sql)
            for row in res:
                if row[0] not in anti and row[0] not in comb and row[0] not in ban:
                    info[row[0]]['anti']['anti_rate'][hero] = row[2]
                    info[row[0]]['anti']['win_rate'][hero] = row[3]
        for hero in comb:
            sql = "SELECT * FROM hero_comb WHERE hero_comb='{}';".format(hero)
            res = self.db.c.execute(sql)
            for row in res:
                if row[0] not in anti and row[0] not in comb and row[0] not in ban:
                    info[row[0]]['comb']['comb_rate'][hero] = row[2]
                    info[row[0]]['comb']['win_rate'][hero] = row[3]
        ans = []
        for hero in all_heroes:
            if hero not in anti and hero not in comb and hero not in ban:
                anti_info = []
                rates = []
                s_anti_rate = 0
                s_anti_win_rate = 0
                for a in anti:
                    antirate = info[hero]['anti']['anti_rate'][a]
                    winrate = info[hero]['anti']['win_rate'][a]
                    rates.append(antirate)
                    s_anti_rate += antirate
                    s_anti_win_rate += winrate
                    s = str(antirate).rjust(6, ' ')  # + '|' + str(winrate).rjust(5, ' ')
                    anti_info.append(s)
                anti_info = ' '.join(anti_info)
                anti_info += ' =' + str(round(s_anti_rate, 2)).rjust(5, ' ')
                comb_info = []
                s_comb_rate = 0
                s_comb_win_rate = 0
                for c in comb:
                    combrate = info[hero]['comb']['comb_rate'][c]
                    winrate = info[hero]['comb']['win_rate'][c]
                    rates.append(combrate)
                    s_comb_rate += combrate
                    s_comb_win_rate += winrate
                    s = str(combrate).rjust(6, ' ')  # + '|' + str(winrate).rjust(5, ' ')
                    comb_info.append(s)
                comb_info = ' '.join(comb_info)
                comb_info += ' =' + str(round(s_comb_rate, 2)).rjust(5, ' ')
                tot_rate = s_anti_rate + s_comb_rate
                tot_win_rate = (s_anti_win_rate + s_comb_win_rate) / (len(anti) + len(comb))
                rate_std = np.std(rates, ddof=1)
                eva = tot_win_rate + tot_rate - rate_std
                tot_info = str(round(tot_rate, 2)) + '|' + str(round(rate_std, 2)) + \
                    '|' + str(round(tot_win_rate, 2)) + '=' + str(round(eva, 2))
                ans.append((hero, anti_info, comb_info, tot_info, eva))
        return sorted(ans, reverse=True, key=lambda x: x[4])
