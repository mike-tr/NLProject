import random

# def f(t, a):
#     c = 0
#     i = -t + a
#     while i <= t:
#         print(i)
#         i += 1
#         c += 1
#     print(c)

# f(5,0)
# f(5,0.5)


def randoms(tries):
    i = 0
    dic = {}
    # for j in range(1,11):
    #     dic[j] = 0
    dic[1] = dic[10] = 0
    while i < tries:
        i += 1
        r = random.randint(1, 10)
        if not 2 <= r <= 9:
            dic[r] += 1
    return dic, dic[10] > dic[1]


print(randoms(100000))
