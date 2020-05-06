import tkinter
from data import Data
from tkinter import ttk


# 更新对手和队友英雄信息
def update_database():
    # data.update_heroes_table()
    data.update_hero_anti_table()
    data.update_hero_comb_table()
    return


def clear_heroes():
    global lst_hero_anti
    global lst_hero_comb
    lst_hero_anti = []
    lst_hero_comb = []
    label_anti['text'] = "对手英雄："
    label_comb['text'] = "队友英雄："
    return


def add_comb():
    if len(lst_hero_comb) > 3:
        return
    hero = combo_box_hero.get()
    if hero not in hero_name_list:
        return
    if hero in lst_hero_comb or hero in lst_hero_anti:
        return
    lst_hero_comb.append(hero)
    text = "队友英雄：" + ', '.join(lst_hero_comb)
    label_comb['text'] = text
    return


def add_anti():
    if len(lst_hero_anti) > 4:
        return
    hero = combo_box_hero.get()
    if hero not in hero_name_list:
        return
    if hero in lst_hero_comb or hero in lst_hero_anti:
        return
    lst_hero_anti.append(hero)
    text = "对手英雄：" + ', '.join(lst_hero_anti)
    label_anti['text'] = text
    return


def calc_recommendation():
    res = data.calc(lst_hero_anti, lst_hero_comb, lst_ban)
    items = tree.get_children()
    for item in items:
        tree.delete(item)
    for i in range(len(res)):
        tree.insert("", i * 2, text="", values=(str(i) + '. ' + res[i][0], res[i][1], res[i][3]))
        tree.insert("", i * 2 + 1, text="", values=("", res[i][2], ""))
    return


# 主窗口设置
window = tkinter.Tk()
window.wm_attributes('-topmost', 1)
window.title("Dota2 Picker V1.0 by CDKJ.LY")
window.geometry('500x1000+0+10')
window.resizable(0, 0)

# 对手英雄与队友英雄
lst_hero_anti = []
lst_hero_comb = []
lst_ban = []
data = Data()

# 英雄列表
hero_name_list = data.get_hero_names_zh()
combo_box_hero = ttk.Combobox(window)
combo_box_hero['values'] = hero_name_list
combo_box_hero.place(x=20, y=20)

# 按钮
btn_add_comb = tkinter.Button(window, text="添加队友", command=add_comb)
btn_add_anti = tkinter.Button(window, text="添加对手", command=add_anti)
btn_clear = tkinter.Button(window, text="清空", command=clear_heroes)
btn_calc = tkinter.Button(window, text="计算", command=calc_recommendation)
btn_update_db = tkinter.Button(window, text="更新数据库", command=update_database)
btn_add_comb.place(x=260, y=17)
btn_add_anti.place(x=200, y=17)
btn_clear.place(x=330, y=17)
btn_calc.place(x=370, y=17)
btn_update_db.place(x=410, y=17)

# label
label_anti = tkinter.Label(window, text="对手英雄：")
label_comb = tkinter.Label(window, text="队友英雄：")
label_anti.place(x=20, y=60)
label_comb.place(x=20, y=85)

# table
columns = ['英雄', '对手与对手', '整体评价']
col_width = [80, 260, 120]
tree = ttk.Treeview(window, height=40, columns=columns, show="headings")
tree.place(x=20, y=120)
length = len(columns)
for i in range(length):
    tree.column(columns[i], width=col_width[i])
    tree.heading(columns[i], text=columns[i])
window.mainloop()
