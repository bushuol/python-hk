class Solution(object):
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        n = len(s)
        maxL, maxR, max = 0, 0, 0
        for i in range(n):
            # 长度为偶数的回文字符串
            start = i
            end = i + 1
            while start >= 0 and end < n:
                if s[start] == s[end]:
                    if end - start + 1 > max:
                        max = end - start + 1
                        maxL = start
                        maxR = end
                    start -= 1
                    end += 1
                else:
                    break

            # 长度为奇数的回文子串
            start = i - 1
            end = i + 1
            while start >= 0 and end < n:
                if s[start] == s[end]:
                    if end - start + 1 > max:
                        max = end - start + 1
                        maxL = start
                        maxR = end
                    start -= 1
                    end += 1
                else:
                    break
        return s[maxL:maxR + 1]



