import tracemalloc
import sys

sys.path.append('..')
sys.path.append('../src')

import learner
import config

# Store 25 frames
tracemalloc.start(25)

snapshot1 = tracemalloc.take_snapshot()

alpha_zero = learner.Leaner(config.config)
# alpha_zero.load_samples()
# ... run your application ...

snapshot2 = tracemalloc.take_snapshot()
top_stats = snapshot2.compare_to(snapshot1, 'lineno')

# pick the biggest memory block
stat = top_stats[0]
print("%s memory blocks: %.1f KiB" % (stat.count, stat.size / 1024))
for line in stat.traceback.format():
    print(line)
    
print("[ Top 10 differences ]")
for stat in top_stats[:10]:
    print(stat)