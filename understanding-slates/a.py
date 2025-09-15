import os
from collections import defaultdict

header = None
d = defaultdict(list)
with open('img_labels.csv', 'r') as in_f:
    in_lines = in_f.readlines()
    header = in_lines[0]
    for row in in_lines[1:]:
        guid = row.split('_')[0][1:]
        d[guid].append(row)

for guid, rows in d.items():

    with open(f'241202-aapb-collaboration-27-f/{guid}.csv', 'w') as out_f:
        out_f.write(header)
        for row in rows:
            out_f.write(row)
