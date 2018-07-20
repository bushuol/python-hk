# -*- coding: UTF-8 -*-
class Solution1(object):
    s = 'noon abba shdshj fsfs'
    def longestPalindrome(self,s):
        """

        :type s: str
        :rtype: str
        """
        lens=len(s)
        if lens<2:
            return s
        maxlen=0
        start=0
        for i in range(lens):
            for j in range(i+1,lens):
                begin=i
                end=j
                while begin<end:
                    if s[begin]!=s[end]:
                        break
                    begin+=1
                    end-=1
                if begin>=end and j-i>maxlen:
                    maxlen=j-i+1
                    start=i
        if maxlen>0:
            return s[start:maxlen]
        return None

