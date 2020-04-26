import random


def calonce(randomtimes):
    res = 0
    normal = [0 for _ in range(10)]
    special = [0 for _ in range(4)]
    cnt = 0
    for i in range(randomtimes):
        res += 800
        choice = random.randint(1, 100)
        if choice <= 3:
            nextchoice = random.randint(0, 3)
            if special[nextchoice]:
                res -= 400
            else:
                special[nextchoice] = 1
                cnt += 1
        else:
            nextchoice = random.randint(0, 9)
            if normal[nextchoice]:
                res -= 400
            else:
                normal[nextchoice] = 1
                cnt += 1
        if cnt == 14:
            break
    for n in normal:
        if not n:
            res += 5000
    for s in special:
        if not s:
            res += 10000
    return res

ans = [0 for _ in range(100)]
ans[0] = 90000
for rt in range(1, 100):
    for trytimes in range(10000):
        ans[rt] += calonce(rt)
    ans[rt] /= 10000
print(ans)
myans = min(ans)
print(myans, ans.index(myans))
