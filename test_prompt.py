import cProfile
import pstats

import short_pwd

cProfile.run("short_pwd.main()", "prompt_stats")

stats = pstats.Stats("prompt_stats")
stats.strip_dirs().sort_stats("cumulative").print_stats(10)
