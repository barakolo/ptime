import time
import operator
'''
## Based on the following idea:
def func1():
    print 'func1'
    
def func2():
    print 'func2'
    
func1_backup = func1
func2_backup = func2
globals()['func1'] = func2
func1()
func2
globals()['func1']
Out[41]: 
<function __main__.func2>
globals()['func1']()
func2
func1_backup()
func1
'''
known_funcs = dict()
saved_fns = ['get_wrapper_names', 'gen_tgraph', 'gen_wrappers', 'gen_wrapper']

def get_wrapper_names(fname):
    wname = 'wrapper_%s' % fname
    tavg_name = wname + '_time_avg'
    tcnt_name = wname + '_time_cnt'
    return wname, tavg_name, tcnt_name

def gen_wrapper(fn, fname, module=None):
    import time
    if module is None:
        dglobals = globals()
    else:
        dglobals = module.__dict__
    wname, tavg_name, tcnt_name = get_wrapper_names(fname)
    def foo(*args, **kwargs):
        tstart = time.time()
        res = fn(*args, **kwargs)
        old_tcnt, old_tavg = globals()[tcnt_name], globals()[tavg_name]
        globals()[tavg_name] = ((old_tavg * old_tcnt) + (time.time() - tstart))\
                               / float(old_tcnt + 1)
        globals()[tcnt_name] += 1
        return res
    globals()[tcnt_name] = 0.0
    globals()[tavg_name] = 0.0
    dglobals[fname] = foo
    foo.__name__ = wname
    return foo

def gen_wrappers(verbose=False, related_modules=['statistics', 'data_structures'], start_module=None):
    if start_module is None:
        nglobals = list(globals().keys())
        dglobals = globals()
    else:
        nglobals = start_module.__dict__.keys()
        dglobals = start_module.__dict__
    for key in nglobals:
        if isinstance(dglobals[key], type(lambda x: x)) and key not in saved_fns:
            if verbose:
                print "[+] Wrapping %s..." % key
            known_funcs[key] = gen_wrapper(dglobals[key], key, module=start_module)
        if isinstance(dglobals[key], type(time)) and dglobals[key].__name__ in related_modules:
            if verbose:
                print "[+] Wrapping module %s..." % key
            gen_wrappers(verbose=verbose, start_module=dglobals[key])
    print "[+] Done creating wrappers."

def gen_tgraph(cut_count=10):
    '''
    :param cut_count: 
    :return: Generate nice bar graph using matplotlib of the time-consuming functions,
     Cut to cut_count functions max.
    '''
    import operator
    import numpy as np
    import matplotlib.pyplot as plt
    plt.rcdefaults()
    fig, ax = plt.subplots()
    avg_time = []
    for fname in known_funcs:
        wname, tavg_name, tcnt_name = get_wrapper_names(fname)
        avg_time.append(globals()[tavg_name])

    # filter functions, only upper than zero.
    arr = zip(known_funcs, avg_time)
    arr.sort(key=operator.itemgetter(1), reverse=True)
    arr = filter(lambda x: x[1] > 0, arr)
    arr = arr[:cut_count]
    fnames, avg_time = map(lambda x: x[0], arr), map(lambda x: x[1], arr)
    y_pos = np.arange(len(fnames))
    error = [0 for i in xrange(len(fnames))]
    # draw the functions.
    print 'aasdas1'
    ax.barh(y_pos, avg_time, xerr=error, align='center', color='red', ecolor='black')
    print 'aasdas2'
    ax.set_yticks(y_pos)
    ax.set_yticklabels(fnames)
    ax.invert_yaxis()
    ax.set_xlabel('Average time')
    ax.set_title('Functions runtime assesment')
    print 'aasdas3'
    plt.show()

def gen_tarr(cut_count=10):
    '''
    :param cut_count: 
    :return: Get sorted list from the most-time consuming function to the last, cut the first cut_count functions. 
    '''
    avg_time = []
    for fname in known_funcs:
        wname, tavg_name, tcnt_name = get_wrapper_names(fname)
        avg_time.append(globals()[tavg_name])

    # filter functions, only upper than zero.
    arr = zip(known_funcs, avg_time)
    arr.sort(key=operator.itemgetter(1), reverse=True)
    arr = filter(lambda x: x[1] > 0, arr)
    arr = arr[:cut_count]
    return arr
