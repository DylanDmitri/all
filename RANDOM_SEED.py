from itertools import chain
from random import choice
import string


def longestPalindrome(s):
    """
    :type s: str
    :rtype: str
    """

    if len(s) < 2:
        return s

    def zoom(left,right):

        if left == -1 or right == len(s) or s[left] != s[right]:
            return left+1,right

        return zoom(left - 1,right + 1)

    left,right = max(chain(*((zoom(i,i),zoom(i,i + 1)) for i in range(len(s) - 1))),key=lambda t:t[1] - t[0])
    return s[left:right]


for trial in range(200):
    letters = 000
    calls = 0
    r = ''.join(choice(string.ascii_lowercase) for _ in range(letters))
    longestPalindrome(r)
    print(calls)

