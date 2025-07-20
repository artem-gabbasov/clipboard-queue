from screen_badge import BadgeManager
import time

with BadgeManager():
    time.sleep(2)

print("quit called")

time.sleep(2)
