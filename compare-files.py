import os
import yaml

class Metrics:
    def __init__(self, host):
        self.metrics = {}
        self.host = host

    def fillMetrics(self, metrics):
        my_stressor = ""
        for metric in metrics:
            for k,v in metric.items():
                if k == 'stressor':
                    my_stressor = v
                if my_stressor not in self.metrics.keys():
                    self.metrics[my_stressor] = {}
                else:
                    if k in self.metrics[my_stressor].keys():
                        self.metrics[my_stressor][k].append(v)
                    else:
                        self.metrics[my_stressor][k] = [v]

def readSystemInfo(nodeInfo) :
    sysInfo = {}
    for key in nodeInfo:
         sysInfo[key] = nodeInfo[key]
    return sysInfo

def validateSysInfo():
    from colorama import Fore as FORE
    from colorama import Style as STYLE
    for key in sysInfo:
        if all (val==sysInfo[key][0] for val in sysInfo[key]):
            print (FORE.GREEN + 'sysInfo.[' + key + ']: OK')
        else:
            print (FORE.RED + 'sysInfo.[' + key + ']: FAIL')
    print (STYLE.RESET_ALL)


if __name__=='__main__':
    host_metrics = {}
    for file in os.listdir():
        if file.endswith(".yaml"):
            fd = open(file, 'r')
            data = yaml.safe_load(fd)
            for key in data.keys():
                if key == 'system-info':
                    sys_info = readSystemInfo (data[key])
                    if sys_info['hostname'] not in host_metrics.keys():
                        my_metrics = Metrics(sys_info['hostname'])
                        host_metrics[sys_info['hostname']] = my_metrics
                    else:
                        my_metrics = host_metrics['hostname']
                elif key=='times':
                    pass
                elif key=='thermal-zones':
                    pass
                else:
                    my_metrics.fillMetrics(data[key])
            break
    for k,v in host_metrics.items():
        print (host_metrics[k].metrics)
