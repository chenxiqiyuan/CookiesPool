'''
@Description: 运行整个项目
@Author: chenxi
@Date: 2019-10-05 22:16:42
@LastEditTime: 2019-11-28 21:58:07
@LastEditors: chenxi
'''
from cookiespool.scheduler import Scheduler

def main():
    s = Scheduler()
    s.run()
    
if __name__ == '__main__':
    main()