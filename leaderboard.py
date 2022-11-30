import time
import _thread, threading
import glob
import pandas as pd
import json

def quit_function(fn_name):
    print('{0} took too long'.format(fn_name))
    _thread.interrupt_main() # raises KeyboardInterrupt

def exit_after(s):
    '''
    use as decorator to exit process if 
    function takes longer than s seconds
    '''
    def outer(fn):
        def inner(*args, **kwargs):
            timer = threading.Timer(s, quit_function, args=[fn.__name__])
            timer.start()
            try:
                tic = time.time()
                _ = fn(*args, **kwargs)
                toc = time.time()
            finally:
                timer.cancel()
            return toc-tic
        return inner
    return outer

# Execute script for up to 10 mins
@exit_after(10*60)
def script(path):
    """Executes python script found at path"""
    exec(open(path).read())

scripts = glob.glob('*/day*/part*.py')

try:
    with open('log.json','r') as fp:
        results = json.loads(fp)
except:
    # log file not found
    results = {}
    
for s in scripts:
    try:
        results[s] = script(s)
    except:
        results[s] = None

with open('log.json', 'w') as fp:
    json.dump(results, fp)

df = pd.DataFrame.from_dict(data = results, orient = 'index').reset_index()
df = pd.concat([
    df['index'].str.split('\\', expand=True),
    df[[0]]],
    axis=1
)
df.columns = ["whomst'd've'ly", 'day', 'part', 'time']
print(df.sort_values(['day','time']))