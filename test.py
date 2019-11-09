import time

to = time.time() + .2

while time.time() < to:
    print(time.time())