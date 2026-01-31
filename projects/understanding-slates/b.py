import csv 

r = csv.DictReader(open('understanding-slates/golds/cpb-aacip-0a5bab74298.csv'))
for row in r:
    print(row)
