import cProfile

pr = cProfile.Profile()
pr.enable()

# code to profile

pr.disable()
pr.print_stats(sort="time")
