

"""argparser를 통해 콘솔 입력 옵션을 파싱한다. 

https://docs.python.org/ko/3/howto/argparse.html

"""

import argparse

parser = argparse.ArgumentParser(description='Test')   

parser.add_argument('--num', type = int, default = 5, help='number test')

args = parser.parse_args()
print('num is ', args.num)
print('type is', type(args.num))

for i in range(args.num):
  print(i)


# python 05_1_argparse.py --num 3 등으로 옵션 실행
