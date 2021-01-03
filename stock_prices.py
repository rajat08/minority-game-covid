# coding: utf-8
from pylab import *
from numpy import *
from minoritygame import *

fig = figure(1,figsize=(6,4))

for n in range(5):
    sim = System(T=1000,N=101, m=3,s=2)
    sim.run()
    plot(sim.Prices)

xlabel(r'$t$')
ylabel(r'$Prices$')
fig.set_tight_layout(True)
savefig('prices.png', format='png',bbox_inches='tight')

fig.clf()
N = 101
syms = ['ro-','gs-','bd-']
s = [2, 4, 6]
for i in range(len(s)):
    Y = []
    X = []
    for m in range(1,15):
        x = []
        y = []
        for t in range(10):
            sim = System(T=200,N=N, m=m,s=s[i])
            sim.run()
            x.append(float(2**m)/float(N))
            y.append(var(sim.D)/float(N))
        X.append(mean(x))
        Y.append(mean(y))
        print('m='+str(m))
    plot(X,Y,syms[i],label='s='+str(s[i]))
    print('s='+str(s[i]))

xscale('log')
yscale('log')
xlabel(r'$2^{m}/N$')
ylabel(r'$\sigma^2/N$')
legend(loc='best')
fig.set_tight_layout(True)
savefig('variance-vs-m.png', format='png',bbox_inches='tight')

fig.clf()

X = []
Y = []
N = 101
for m in range(1,10):
    x = []
    y = []
    for t in range(10):
        sim = System(T=200,N=N, m=m)
        sim.run()
        x.append(float(2**m)/float(N))
        y.append(mean(sim.SuccessRates))
    X.append(mean(x))
    Y.append(mean(y))
    print('m='+str(m))

plot(X,Y,'o-')
xscale('log')
xlabel(r'$2^{m}/N$')
ylabel(r'$success\ rate$')
savefig('success_rate-vs-m.png', format='png',bbox_inches='tight')
close(fig)