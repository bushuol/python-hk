class Solution:
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        L = len(s)
        len_max = [0, 0, 0]  # 长度 开始 结束的index
        if L == 0:  # s为空的情况
            return ''
        for i in range(L):
            ##aba奇数个形式
            r = i + 1
            l = i - 1
            while (l >= 0 and r < L):
                if s[l] != s[r]:
                    break
                l -= 1
                r += 1
            if (l >= 0 and r < L) or (l == -1 and r < L) or (l >= 0 and r == L):
                len_temp = r - l - 1
                if len_temp > len_max[0]:  # 更新最大回文子串
                    len_max = [len_temp, l + 1, r]
            else:
                len_temp = r - l - 1
                if len_temp > len_max[0]:  # 更新最大回文子串
                    len_max = [len_temp, l + 1, r]
            # abba偶数个形式
            l = i
            r = i + 1
            while (l >= 0 and r < L):
                if s[l] != s[r]:
                    break
                l -= 1
                r += 1
            if (l >= 0 and r < L) or (l == -1 and r < L) or (l >= 0 and r == L):
                len_temp = r - l - 1
                if len_temp > len_max[0]:  # 更新最大回文子串
                    len_max = [len_temp, l + 1, r]
            else:
                len_temp = r - l - 1
                if len_temp > len_max[0]:  # 更新最大回文子串
                    len_max = [len_temp, l + 1, r]

        return s[len_max[1]:len_max[2]]
