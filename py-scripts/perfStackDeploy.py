"""Perf Stack Deployment.

Usage:
  perfStackDeploy.py REPOSITORY FOLDER
  perfStackDeploy.py (-h | --help)
  perfStackDeploy.py --version

Arguments:
  REPOSITORY    Docker repository to which you have access. It will be used as the testing image.
  FOLDER        Directory containing all the neccessary documents (track.json, index.json, data.json)

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
from docopt import docopt
import subprocess, shlex, sys, time, os, fileinput


def cmd(shellCommand):
    proc = subprocess.Popen(shlex.split(shellCommand), stdout=subprocess.PIPE)
    return proc.communicate()[0].decode("utf-8")

def getRallyNodes():
    allNodes = cmd("oc get nodes -o=jsonpath='{.items[*].metadata.name}'").split(" ")
    print(allNodes)

    esPod = cmd("oc get po -l component=elasticsearch -o name")
    print(esPod)

    esNode = cmd("oc get {} -o jsonpath='{{.spec.nodeName}}'".format(esPod))
    esNode = [esNode]
    print(esNode)

    master = cmd("oc get nodes -l node-role.kubernetes.io/master -o jsonpath='{.items[*].metadata.name}'").split(" ")
    print(master)

    removeNodes = master + esNode
    print(removeNodes)


    for i in removeNodes:
        allNodes.remove(i)

    return allNodes

def rep(filePath, old, new):
    for line in fileinput.input([filePath], inplace=True):
        print(line.replace(old, new), end='')



def main(arguments):
    rallyFolder = os.path.basename(os.path.dirname(arguments["FOLDER"]))

    commands = [
        "oc create -f manifests/dep-etcd.yaml",
        "oc create -f manifests/svc-etcd.yaml",
        "oc project openshift-monitoring",
        "oc create -f manifests/cm-dashboard-logging.yaml",
        "oc create -f manifests/dep-grafana.yaml",
        "oc create -f manifests/svc-grafana.yaml",
        "oc patch route grafana -p '{\"spec\":{\"to\":{\"name\":\"grafana-logging\"}}}'",
        "oc project openshift-logging",
    ]

    for i in commands:
        print(i)
        print(cmd(i))


    allNodes = getRallyNodes()
    print(allNodes)

    print("Labeling...")
    for node in allNodes:
        cmd("oc label nodes {} esrally=present".format(node))


    nodeCount = len(allNodes)
    print(nodeCount)

    rep("start/esrally-container/copy/scr", "<rallyFolder-placeholder>", rallyFolder)
    rep("manifests/job-rally.yaml", "<node-number-placeholder>", "\"{}\"".format(nodeCount))
    rep("manifests/is-rally.yaml", "<docker-image-placeholder>", arguments["REPOSITORY"])
    

    commands = [
        "tar -zcvf rallyFolder.tar.gz {}".format(arguments["FOLDER"]),
        "mv rallyFolder.tar.gz start/esrally-container/copy/",
        "mkdir -p start/esrally-container/secret",
        "oc extract secrets/elasticsearch --to=start/esrally-container/secret --confirm",
        "docker build -t {} ./start/esrally-container".format(arguments["REPOSITORY"]),
        "docker push {}".format(arguments["REPOSITORY"]),
        "oc create -f manifests/is-rally.yaml",
        "oc create -f manifests/job-rally.yaml",
    ]
    

    for i in commands:
        print(i)
        print(cmd(i))


    rep("start/esrally-container/copy/scr", rallyFolder, "<rallyFolder-placeholder>")
    rep("manifests/job-rally.yaml", "\"{}\"".format(nodeCount), "<node-number-placeholder>")
    rep("manifests/is-rally.yaml", arguments["REPOSITORY"], "<docker-image-placeholder>")

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Performance Stack Deploy Aplha')
    print(arguments)
    main(arguments)
