import time
from algolink.config import DISK_CACHE

t1 = time.time()
gdfgg = DISK_CACHE["woe_chips"]
print(gdfgg.transform([0.5]), time.time() - t1)
