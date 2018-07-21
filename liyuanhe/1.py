def manacher(s):
    s = '#' + '#'.join(s) + '#'  # step1
    RL = [0] * len(s)
    MaxRight = 0
    Pos = 0
    Maxlen = 0
    for i in range(len(s)):
        if i < MaxRight:
            RL[i] = min(RL[2 * Pos - i], MaxRight - i)
        else:
            RL[i] = 1
        while i - RL[i] >= 0 and i + RL[i] < len(s) and s[i - RL[i]] == s[i + RL[i]]:
            RL[i] += 1
        if RL[i] + i - 1 > MaxRight:
            MaxRight = RL[i] + i - 1
            Pos = i
        Maxlen = max(Maxlen, RL[i])
    s = s[RL.index(Maxlen) - (Maxlen - 1):RL.index(Maxlen) + (Maxlen - 1)]
    s = s.replace('#', '')
    return s
print(manacher('ufdgwehgwfghfejjhhhhhher'))