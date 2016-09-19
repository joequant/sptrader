import strategy.sample
import sys
import os

def run(name, id, kwargs):
    if name == "sample":
        modpath = os.path.dirname(os.path.realpath(__file__))
        logpath = os.path.join(modpath, '../data/log-%s-%s.txt' % \
                               (name, str(id)))
        sys.stdout = open(logpath, "w")
        kwargs['newdata'] = True
        kwargs['keepalive'] = True
        kwargs['debug'] = True
        kwargs['streaming'] = True
        return sample.run(kwargs)

if __name__ == '__main__':
    run("sample", 1)
