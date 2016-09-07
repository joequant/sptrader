import strategy.sample

def run(name, id):
    if name == "sample":
        sample.run({"newdata": True,
                    "keepalive": True,
                    "debug" : True})

if __name__ == '__main__':
    run("sample", "start")
