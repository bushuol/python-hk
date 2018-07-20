# 枚举法求最长回文子串

ch=input()
chlen=len(ch)
maxcount=0
for j in range(chlen):
    for k in range(j,chlen):
        count=0
        m=j
        n=k
        while n>=1 and m<chlen:
            if ch[m]==ch[n]:
                m=m+1
                n=n-1
            else:
                break
        else:
            count=k-j+1
            if maxcount<count:
                maxcount=count
                start=j     #保存maxcount的开头和结尾，便于输出
                end=k
print("最长回文子串：",ch[start:end+1])
print("最长回文子串的长度：",maxcount)

