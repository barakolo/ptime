### ptime / Simple Python Profiler for the masses by Barak Sternberg ###
Simple python profiler, to get the most time consuming functions.

* to draw the time consuming functions in scale (using barh graph) - one will need numpy, matplotlib installed.

Usage:

*** Method 1 - profile imported modules: ***
# Use the following code to inspect x, y modules:
import x
import y
execfile('ptime.py')
gen_wrappers(verbose=True, related_modules=['x', 'y'])
### YOUR CODE HERE ###
gen_tgraph()

*** Method 2 - profile code of current file: ***
# profile f1, f2, f3 functions.
import math
import random

def f1(a):
    lol = a * 1.0
    for i in xrange(10000):
        lol *= (i+1) / (2 ** i)
    return lol

def f2(a):
    s = 0.0
    for i in xrange(10000):
        s += math.log(a + (i * 321), 2)
    return s

def f3(a):
    print "nope."

execfile('ptime.py')
gen_wrappers(True)

for i in xrange(100):
    a = [f1, f2, f3]
    a[int(len(a) * random.random())](i)

gen_tgraph()





