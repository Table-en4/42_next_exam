Input
hidenp("abc", "a1b2c3")
Output
True
Input
hidenp("ace", "abcde")
Output
True
Input
hidenp("aec", "abcde")
Output
False
Input
hidenp("", "abc")
Output
True
Input
hidenp("abc", "ab")
Output
False
Input
hidenp("aaaa", "aaa")
Output
False
Input
hidenp("sing","subsequence testing")
Output
True