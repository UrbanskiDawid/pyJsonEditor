""" generete fun stats for this project """

import os
import matplotlib.pyplot as plt

OUT_FN='DOC/stats_boilerplate.png'
IGNORED_FOLDERS = ['__pycache__', '.git']

##   FIND ALL FILES ##
f = {}
for (dirpath, dirnames, filenames) in os.walk('.'):
    for i in filenames:
        fn = os.path.join(dirpath, i)
        num_lines = sum(1 for line in open(fn, errors="ignore"))
        f[fn] = {'num_lines': num_lines}

## AGREGATE DATA ##
stats = {
    'code': 0,
    'boilerplate': 0
}
for k, v in f.items():
    if k in IGNORED_FOLDERS:
        continue
    if 'pyjsonedit' in k:
        stats['code'] += 1
    else:
        stats['boilerplate'] += 1

## Plot Pie
labels = list(stats.keys())
sizes = list(stats.values())
explode = (0, 0.1)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=0)
ax1.axis('equal')
ax1.set_title('my code vs boilerplate in this project')
plt.savefig(OUT_FN, transparent=False)
