import time
def timer():
    start_time=[2,7,12,16]
    for i in start_time:
        if time.localtime()[3] == i:
            return True
    return False