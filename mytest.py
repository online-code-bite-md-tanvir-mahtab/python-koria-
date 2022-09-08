from threading import Thread


current_list  = []

current_list = [i for i in range(0,10)]
t1 = Thread(target=current_list)
t1.start()
t1.join()
print(current_list)