import subprocess, shlex, sys, time

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
    label = subprocess.Popen(shlex.split("oc label nodes {} esrally=present".format(node)))


nodeCount = len(allNodes)
print(nodeCount)

subprocess.Popen(shlex.split("sed -i \'s/<node-number-placeholder>/{}/g\' manifests/job-rally.yaml".format(nodeCount)), stdout=subprocess.PIPE)

subprocess.Popen(shlex.split("sed -i \'s/<node-number-placeholder>/\"{}\"/g\' manifests/po-bootstrap.yaml".format(nodeCount)), stdout=subprocess.PIPE)
subprocess.Popen(shlex.split("oc create -f manifests/po-bootstrap.yaml"), stdout=subprocess.PIPE)

yaml = ""
while "reason: Completed" not in yaml:
    bootYaml = subprocess.Popen(shlex.split("oc get pod bootstrap -o yaml"), stdout=subprocess.PIPE)
    yaml = bootYaml.communicate()[0].decode("utf-8")
    time.sleep(3)

