from progress.bar import Bar

with Bar('Processing', max=20) as bar:
    for i in range(20):
        # Do some work
        bar.next()