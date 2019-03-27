# First error. Prometheus does not see ES for some reason

cd ~/projects/elasticsearch-performance-testing

oc create -f dep-etcd.yaml
oc create -f svc-etcd.yaml

oc project openshift-monitoring

oc create -f cm-dashboard-logging
oc create -f dep-grafana
oc create -f svc-grafana

oc patch route grafana -p '{"spec":{"to":{"name":"grafana-logging"}}}'

oc project openshift-logging


# OK ^^^



python3 negativeNodeLabel.py

oc delete po bootstrap



cd start/secret

rm *

oc extract secrets/elasticsearch

cd -

docker build -t docker.io/vladmasarik/hackfest-dep /home/vmasarik/projects/elasticsearch-performance-testing/start
docker push docker.io/vladmasarik/hackfest-dep

oc create -f is-rally.yaml

oc create -f job-rell.yaml

python3 revertToPlaceholders.py
