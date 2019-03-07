from matplotlib import pyplot as plt
import sys
m = 10000000000
'''
for name in sys.argv[1:]:
    with open(name, "r") as f:
        r = f.read()
        m = min(m,len( r.split("\n")))
'''
for name in sys.argv[1:]:
    with open(name, "r") as f:
        r = f.read()
        l = [a for a in r.split("\n") if a != ""]
        l = [float(a) for a in l[:m]]
        l = [a for a in l if a < 100]

        s  = sorted(l)
        rank = [i/len(l) for i in range(len(l))]
        plt.scatter(x = sorted(l), y = rank, label = name)
plt.legend()
plt.savefig("band_comparison.png")
