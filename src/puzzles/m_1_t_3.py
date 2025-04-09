def rle(s: str) -> str:
    res, count = "", 1
    for i in range(len(s)):
        if i + 1 >= len(s) or s[i] != s[i + 1]:
            res += s[i] + str(count)
            count = 1
        else:
            count += 1
    return res
