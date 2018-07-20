class LPS:
    def manacher(self):

        s = '#' + '#'.join(self.string) + '#'
        lens = len(s)

        f = []

        maxj = 0

        maxl = 0

        maxd = 0

        for i in range(lens):

            if maxl > i:

                count = min(maxl - i, int(f[2 * maxj - i] / 2) + 1)

            else:

                count = 1

            while i - count >= 0 and i + count < lens and s[i - count] == s[i + count]:

                count += 1

            if (i - 1 + count) > maxl:

                maxl, maxj = i - 1 + count, i

            f.append(count * 2 - 1)

            maxd = max(maxd, f[i])

        return int((maxd + 1) / 2) - 1
