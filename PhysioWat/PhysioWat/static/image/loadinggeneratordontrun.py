import numpy as np
import matplotlib.pyplot as plt
import random

delta = np.pi/2
shift1 = np.pi*random.random()*2
shift5 = np.pi*random.random()*2
shift3 = np.pi*random.random()*2
shift8 = np.pi*random.random()*2
shift2 = np.pi*random.random()*2
shift6 = np.pi*random.random()*2
shift7 = np.pi*random.random()*2
shift4 = np.pi*random.random()*2
c = np.linspace(-np.pi,np.pi,300)
def drange(start, stop, step):
    r = start
    while r < stop:
        yield r
     	r += step
cnt = 0
for z in drange(-np.pi,np.pi,.01):
    x = np.sin(3 * z + delta)
    y = np.sin(4 * z)
    d = np.sin(3 * (z+shift1) + delta)
    e = np.sin(4 * (z+shift1))
    f = np.sin(3 * (z+shift2) + delta)
    g = np.sin(4 * (z+shift2))
    h = np.sin(3 * (z+shift3) + delta)
    i = np.sin(4 * (z+shift3))
    j = np.sin(3 * (z+shift4) + delta)
    k = np.sin(4 * (z+shift4))
    l = np.sin(3 * (z+shift5) + delta)
    m = np.sin(4 * (z+shift5))
    n = np.sin(3 * (z+shift6) + delta)
    o = np.sin(4 * (z+shift6))
    p = np.sin(3 * (z+shift7) + delta)
    q = np.sin(4 * (z+shift7))
    r = np.sin(3 * (z+shift8) + delta)
    s = np.sin(4 * (z+shift8))
    a = np.sin(3 * c + delta)
    b = np.sin(4 * c)
    #plt.plot(a, b,color='k',linewidth=1.0,zorder=3)
    area1 = np.pi * (15 * np.sin(z))**2
    area2 = np.pi * (15 * np.sin(z+shift1))**2
    area3 = np.pi * (15 * np.sin(z+shift2))**2
    area4 = np.pi * (15 * np.sin(z+shift3))**2
    area5 = np.pi * (15 * np.sin(z+shift4))**2
    area6 = np.pi * (15 * np.sin(z+shift5))**2
    area7 = np.pi * (15 * np.sin(z+shift6))**2
    area8 = np.pi * (15 * np.sin(z+shift7))**2
    area9 = np.pi * (15 * np.sin(z+shift8))**2
    plt.scatter(x, y, s=area1, c='k', alpha=1,zorder=4)
    plt.scatter(d, e, s=area2, c='k', alpha=1,zorder=4)
    plt.scatter(f, g, s=area3, c='k', alpha=1,zorder=4)
    plt.scatter(h, i, s=area4, c='k', alpha=1,zorder=4)
    plt.scatter(j, k, s=area5, c='k', alpha=1,zorder=4)
    plt.scatter(l, m, s=area6, c='k', alpha=1,zorder=4)
    plt.scatter(n, o, s=area7, c='k', alpha=1,zorder=4)
    plt.scatter(p, q, s=area8, c='k', alpha=1,zorder=4)
    plt.scatter(r, s, s=area9, c='k', alpha=1,zorder=4)
    plt.axis('off')
    axes = plt.gca()
    axes.set_xlim([-1.5,1.5])
    axes.set_ylim([-1.5,1.5])
    plt.savefig("lis"+str(cnt)+".tif")
    print str(cnt)
    plt.clf()
    cnt += 1
