import os
import yaml
basenames = ['cpu', 'cpu-cache', 'memory', 'network', 'scheduler', 'vm']



sysInfo = {
        'release': [],
        'version': [],
        'machine': [],
        'pagesize': [],
        'cpus': [],
        'cpus-online': []
        }

class Metrics:
    def __init__(self):
        self.metrics = {}

    def fillMetrics(self, metrics):
        pass

def readSystemInfo(nodeInfo) :
    for key in nodeInfo:
        if key in sysInfo.keys():
            sysInfo[key].append(nodeInfo[key])

def validateSysInfo():
    from colorama import Fore as FORE
    from colorama import Style as STYLE
    for key in sysInfo:
        if all (val==sysInfo[key][0] for val in sysInfo[key]):
            print (FORE.GREEN + 'sysInfo.[' + key + ']: OK')
        else:
            print (FORE.RED + 'sysInfo.[' + key + ']: FAIL')
    print (STYLE.RESET_ALL)


for test in basenames:
    for file in os.listdir():
        if file.endswith(test+".yaml"):
            fd = open(file, 'r')
            data = yaml.safe_load(fd)
            for key in data.keys():
                if key == 'system-info':
                    readSystemInfo (data[key])
                elif key=='times':
                    pass
                elif key=='thermal-zones':
                    pass
                else:
                    cpu = Metrics().fillMetrics(data[key])
            break

validateSysInfo()
