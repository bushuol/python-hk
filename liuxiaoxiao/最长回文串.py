class Solution:
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        mmax = 0
        mfrom = 0
        mlen = len(s)
        for i in range(mlen):
            temp = 0
            while temp < i and temp + i < mlen - 1:
                if not s[i - temp - 1] == s[temp + i + 1]:
                    break
                temp += 1
            if mmax < temp * 2 + 1:
                mmax = temp * 2 + 1
                mfrom = i - temp
        for i in range(mlen):
            temp = 0
            while temp <= i and temp + i < mlen - 1:
                if not s[i - temp] == s[temp + i + 1]:
                    break
                temp += 1
            if mmax < temp * 2:
                mmax = temp * 2
                mfrom = i - temp + 1
        return s[mfrom:mfrom + mmax]
