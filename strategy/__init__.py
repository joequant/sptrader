import strategy.sample
import sys

def run(name, id):
    if name == "sample":
        modpath = os.path.dirname(os.path.realpath(__file__))
        logpath = os.path.join(modpath, '../data/log-%s-%s.txt' % \
                               (name, str(id)))
        sys.stdout = open(logpath, "w")
        return sample.run({"newdata": True,
                           "keepalive": True,
                           "debug" : True})

if __name__ == '__main__':
    run("sample", 1)
