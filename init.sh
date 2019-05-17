#!/bin/bash





oc create -f manifests/dep-etcd.yaml
oc create -f manifests/svc-etcd.yaml






oc project openshift-monitoring

oc create -f manifests/cm-dashboard-logging.yaml
oc create -f manifests/dep-grafana.yaml
oc create -f manifests/svc-grafana.yaml

oc patch route grafana -p '{"spec":{"to":{"name":"grafana-logging"}}}'

oc project openshift-logging




python3 py-scripts/negativeNodeLabel.py

oc delete po bootstrap


mkdir -p start/esrally-container/secret
cd start/esrally-container/secret

rm *

oc extract secrets/elasticsearch

cd -

# !!! Put your own images and replace image in Rally ImageStream !!!
docker build -t docker.io/vladmasarik/hackfest-dep ./start/esrally-container
docker push docker.io/vladmasarik/hackfest-dep

oc create -f manifests/is-rally.yaml

oc create -f manifests/job-rally.yaml

python3 py-scripts/revertToPlaceholders.py
