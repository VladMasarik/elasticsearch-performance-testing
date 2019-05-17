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
import subprocess, shlex, sys, time, os


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
        cmd(i)


    allNodes = getRallyNodes()
    print(allNodes)

    print("Labeling...")
    for node in allNodes:
        cmd("oc label nodes {} esrally=present".format(node))


    nodeCount = len(allNodes)
    print(nodeCount)


    

    commands = [
        "tar -zcvf rallyFolder.tar.gz {}".format(arguments["FOLDER"]),
        "mv rallyFolder.tar.gz start/esrally-container/copy/",
        "sed -i \'s/<rallyFolder-placeholder>/{}/g\' start/esrally-container/copy/scr".format(rallyFolder),
        "sed -i \'s/<node-number-placeholder>/{}/g\' manifests/job-rally.yaml".format(nodeCount),
        "sed -i \'s/<docker-image-placeholder>/{}/g\' manifests/is-rally.yaml".format(arguments["REPOSITORY"]),
        "mkdir -p start/esrally-container/secret",
        "oc extract secrets/elasticsearch --to=start/esrally-container/secret --confirm",
        "docker build -t {} ./start/esrally-container".format(arguments["REPOSITORY"]),
        "docker push {}".format(arguments["REPOSITORY"]),
        "oc create -f manifests/is-rally.yaml",
        "oc create -f manifests/job-rally.yaml",
        "sed -i \'s/{}/<node-number-placeholder>/g\' manifests/job-rally.yaml".format(nodeCount),
        "sed -i \'s/{}/<docker-image-placeholder>/g\' manifests/is-rally.yaml".format(arguments["REPOSITORY"]),
        "sed -i \'s/{}/<rallyFolder-placeholder>/g\' start/esrally-container/copy/scr".format(rallyFolder)
    ]
    



    for i in commands:
        print(i)
        cmd(i)


    


    


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Performance Stack Deploy Aplha')
    print(arguments)
    main(arguments)