import subprocess, shlex, sys

res = subprocess.Popen(shlex.split("oc get nodes -o=jsonpath='{.items[*].metadata.name}'"), stdout=subprocess.PIPE)
allNodes = res.communicate()[0].decode("utf-8").split(" ")
print(allNodes)

pod = subprocess.Popen(shlex.split("oc get po -l component=elasticsearch -o name"), stdout=subprocess.PIPE)
esPod = pod.communicate()[0].decode("utf-8")
print(esPod)

node = subprocess.Popen(shlex.split("oc get {} -o jsonpath='{{.spec.nodeName}}'".format(esPod)), stdout=subprocess.PIPE)
esNode = node.communicate()[0].decode("utf-8")
esNode = [esNode]
print(esNode)

master = subprocess.Popen(shlex.split("oc get nodes -l node-role.kubernetes.io/master -o jsonpath='{.items[*].metadata.name}'"), stdout=subprocess.PIPE)
master = master.communicate()[0].decode("utf-8").split(" ")
print(master)

removeNodes = master + esNode
print(removeNodes)

for i in removeNodes:
    allNodes.remove(i)

print(allNodes)
print("Labeling...")
for node in allNodes:
    label = subprocess.Popen(shlex.split("oc label nodes {} esrally=ano".format(node)))

'''
print("Do you want to create job? n")
for i in sys.stdin:
    i.rstrip()
    if i == "n":
        exit()
    else:
        break


print("Creating job...")
subprocess.Popen(shlex.split("oc create -f /home/vmasarik/test/rell-job"))
'''
