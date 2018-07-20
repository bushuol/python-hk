
#coding:utf-8

#预处理
def manacher(s):
    s='#'+'#'.join(s)+'#'

    p=[0]*len(s)
    MaxRight=0
    Pos=0
    MaxLen=0
    for i in range(len(s)):
        if i<MaxRight :
            p[i]=min(p[2*Pos-i],MaxRight-i)#[2*Pos-i] Pos偏左,MaxRight-i Pos偏右
        else:
            p[i]=1


        #尝试扩展，注意处理边界
        while i-p[i]>=0 and i+p[i]<len(s) and  s[i-p[i]]==s[i+p[i]]:
            p[i]+=1

        #更新MaxRight,Pos
        if p[i]+i-1>MaxRight:
            MaxRight=p[i]+i-1
            Pos=i

        #更新最长回文串长度
        MaxLen=max(MaxLen,p[i])
        return MaxLen