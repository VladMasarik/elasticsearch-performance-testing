import subprocess, shlex, json

#curl -X PUT http://172.30.101.100:4001/v2/keys/count -d value=5
#"curl http://172.30.101.100:4001/v2/keys/count?prevValue={} -XPUT -d value=#".format(val, val-1)
#result = subprocess.Popen(shlex.split("curl -X PUT http://172.30.101.100:4001/v2/keys/count -d value=5"), stdout=subprocess.PIPE)


def getVal():
    result = subprocess.Popen(shlex.split("curl http://172.30.101.100:4001/v2/keys/count"), stdout=subprocess.PIPE)
    jsonAnswer = result.communicate()[0].decode("utf-8")
    answer = json.loads(jsonAnswer)
    val = int(answer["node"]["value"])
    print("Get value ={}".format(val))
    return val

def compareSwap(val):
    result = subprocess.Popen(shlex.split("curl http://172.30.101.100:4001/v2/keys/count?prevValue={} -XPUT -d value={}".format(val, val-1)), stdout=subprocess.PIPE)
    ans = json.loads(result.communicate()[0].decode("utf-8"))
    exp = int(ans["node"]["value"])
    print("Change Got=={} ## Expected=={}".format(exp, val - 1))
    return exp == val - 1

def atomicDec():
    while not compareSwap(getVal()):
        pass
    print("Done!")
    return
    


atomicDec()