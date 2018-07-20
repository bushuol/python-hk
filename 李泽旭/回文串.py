def max_substr(string):
  s_list = [s for s in string]
  string = '#' + '#'.join(s_list) + '#'
  max_length = 0
  length = len(string)
  for index in range(0, length):
    r_length = get_length(string, index)
    if max_length < r_length:
      max_length = r_length
  return max_length
 
def get_length(string, index):
  # 循环求出index为中心的最长回文字串
  length = 0
  r_ = len(string)
  for i in range(1,index+1):
    if index+i < r_ and string[index-i] == string[index+i]:
      length += 1
    else:
      break
  return length
 
if __name__ == "__main__":
  result = max_substr("35534321")
  print(result)
