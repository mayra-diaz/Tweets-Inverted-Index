import glob

for filepath in glob.iglob(r'./stopWords/*'):
    print(filepath)