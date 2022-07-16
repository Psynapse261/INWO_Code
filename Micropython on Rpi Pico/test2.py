import time

def blurbCounter(i):
    return_blurb = i*i

    return return_blurb


for k in range (1,21):
    blurb = blurbCounter(k)
    #print("test2 - ",blurb)
    time.sleep(0.1)
