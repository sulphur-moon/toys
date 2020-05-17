# coding=utf-8
import json
from database import Database


def main():
    db = Database()
    hero_names = db.get_hero_names_zh()
    print(hero_names)

    # 生成json_hero文件
    dict_hero = dict()
    sql = "SELECT * FROM heroes;"
    res = db.c.execute(sql)
    dict_hero['选择英雄'] = dict()
    dict_hero['选择英雄']['name_en'] = ''
    dict_hero['选择英雄']['win_rate'] = 0
    dict_hero['选择英雄']['pic_url'] = 'select.png'
    for row in res:
        dict_hero[row[1]] = dict()
        dict_hero[row[1]]['name_en'] = row[0]
        dict_hero[row[1]]['win_rate'] = row[2]
        dict_hero[row[1]]['pic_url'] = row[3]
    json_str = json.dumps(dict_hero, indent=4, ensure_ascii=False)
    print(json_str)
    with open('json_hero.js', 'w', encoding='utf-8') as f:
        f.write("export const hero_dict = ")
        f.write(json_str)
        f.close()

    # 生成json_anti文件
    dict_anti = dict()
    for hero in hero_names:
        dict_anti[hero] = dict()
        sql = "SELECT * FROM hero_anti WHERE hero_anti='{}';".format(hero)
        res = db.c.execute(sql)
        for row in res:
            dict_anti[hero][row[0]] = dict()
            dict_anti[hero][row[0]]["anti_rate"] = row[2]
            dict_anti[hero][row[0]]["win_rate"] = row[3]
    #json_str = json.dumps(dict_anti, indent=4, ensure_ascii=False)
    json_str = json.dumps(dict_anti, indent=4, ensure_ascii=False)
    # print(json_str)
    with open('json_anti.js', 'w', encoding='utf-8') as f:
        f.write("export const anti_dict = ")
        f.write(json_str)
        f.close()

    # 生成json_comb文件
    dict_comb = dict()
    for hero in hero_names:
        dict_comb[hero] = dict()
        sql = "SELECT * FROM hero_comb WHERE hero_comb='{}';".format(hero)
        res = db.c.execute(sql)
        for row in res:
            dict_comb[hero][row[0]] = dict()
            dict_comb[hero][row[0]]["comb_rate"] = row[2]
            dict_comb[hero][row[0]]["win_rate"] = row[3]
    #json_str = json.dumps(dict_anti, indent=4, ensure_ascii=False)
    json_str = json.dumps(dict_comb, indent=4, ensure_ascii=False)
    # print(json_str)
    with open('json_comb.js', 'w', encoding='utf-8') as f:
        f.write("export const comb_dict = ")
        f.write(json_str)
        f.close()
    return


main()
