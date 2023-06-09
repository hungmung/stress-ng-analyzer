import os
import yaml

class Metrics:
    def __init__(self, host):
        self.metrics = {}
        self.host = host

    def __str__(self):
        import pprint
        my_str = ""
        my_str += self.host
        my_str += pprint.pformat(self.metrics)
        return my_str

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


def gather_by_metric(metrics) -> dict:
    all_metrics = {}
    for metric in metrics:
        for test in metric.metrics.keys():
            for measure in metric.metrics[test].keys():
                this_key =  (test, measure)
                this_value = metric.metrics[test][measure]
                if this_key in all_metrics.keys():
                    all_metrics[this_key].extend(this_value)
                else:
                    all_metrics[this_key] =[]
                    all_metrics[this_key].extend(this_value)
    return all_metrics

def validate_metrics(mertics:dict):
    from colorama import Fore as FORE
    from colorama import Style as STYLE
    ok  = FORE.GREEN + "[{}:{}]: OK"
    nok = FORE.RED + "[{}:{}]: NOK {}"
    for key in metrics.keys():
        upper = max(metrics[key])
        lower = min(metrics[key])
        try:
            if (upper - lower)/upper < 0.1:
                print (ok.format(key[0], key[1]))
            else:
                print (nok.format(key[0], key[1], str(metrics[key])))
        except:
            print (STYLE.RESET_ALL + "Do data for {},{}: ()".format(key[0], key[1], str(metrics[key])))
    print (STYLE.RESET_ALL)

host_metrics = []
for file in os.listdir():
    if file.endswith(".yaml"):
        fd = open(file, 'r')
        data = yaml.safe_load(fd)
        for key in data.keys():
            if key == 'system-info':
                sys_info = readSystemInfo (data[key])
                my_host = sys_info['hostname']
                my_metrics = None
                for m in host_metrics:
                    if m.host == my_host:
                        my_metrics = m
                        break
                if not my_metrics:
                    my_metrics = Metrics(my_host)
                    host_metrics.append(my_metrics)
            elif key=='times':
                pass
            elif key=='thermal-zones':
                pass
            else:
                my_metrics.fillMetrics(data[key])
# So now we have a set of metrics, one per host.  We now need to validate
# consistency between hosts. So we have to rearrange into a dict where
# the key is the tuple (stressor, measureand) and the value if a list of
# values from every machine
# We can do this either within the Metrics class possibly, but for now, lets 
# just do it as a function at the top level:

metrics = gather_by_metric(host_metrics)
validate_metrics(metrics)


        
#        if max(v) - min(v) <= 0.1*max(v):
#            print (FORE.GREEN + k + ": OK")
#        else:
#            print (FORE.RED + k + ": NOK - " + sorted(v))
#        print (STYLE.RESET_ALL)
