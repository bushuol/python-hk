str1= "aaasda"
str2 = []
p=[]
def init():
    str2.append('#')
    for i in range(len(str1)):
        str2.append(str1[i])
        str2.append('#')
    for i in range(len(str2)):
        p.append(0)
    print(str2)
    print(p)
def manacher():
    maxx = 0
    ans = 0
    for i in range(len(str2)):
        if maxx > i:
            p[i] = min(maxx-i, p[2*id-i])
        else:
            p[i] = 1
        while (i+p[i]<len(str2) and i - p[i]>=0 and str2[i + p[i]] == str2[i - p[i]] ):
            p[i] += 1;
        if i + p [i] > maxx:
            maxx = i + p[i]
            id = i
        ans = max(ans, p[i]);
        print(p)
    return ans-1
init()
print(manacher())












