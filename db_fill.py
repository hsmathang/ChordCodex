from generators import lazy_full
import time

init_time = time.time()

for chord in lazy_full(1,5):
    print(chord)   

print(time.time() - init_time)