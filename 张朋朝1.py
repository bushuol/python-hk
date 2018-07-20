class Solution(object):

    def isPalindrome(self, s, start, end):
        while start < end:
            if s[start] != s[end]:
                return False
            start += 1
            end -= 1
        return True

    def longestPalindrome(self, s):
        max, left, right = 0, 0, 0
        for i in range(len(s)):
            j = i + 1
            while j < len(s):
                if self.isPalindrome(s, i, j):
                    if (j - i + 1) > max:
                        left, right = i, j
                        max = j - i + 1
                j += 1
        print(left, right, max)
        return s[left:right + 1]



