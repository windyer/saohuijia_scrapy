import time
def timer():
    start_time=[2,7,12,16]
   # start_time=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,0]
    for i in start_time:
        if (time.localtime()[3]+8)%24 == i:
            return True
    return False
