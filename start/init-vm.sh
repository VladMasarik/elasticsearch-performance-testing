oc project openshift-logging

mkdir /data/src/start/secret && cd /data/src/start/secret

oc extract secrets/logging-elasticsearch

cd ..

docker build -t rallyperf .

oc set image ds logging-fluentd fluentd-elasticsearch=openshift/origin-logging-fluentd
oc set image $(oc get dc -o name | grep es) elasticsearch=openshift/origin-logging-elasticsearch5
oc rollout cancel $(oc get dc -o name | grep es)
oc rollout latest $(oc get dc -o name | grep es)
oc set image deploymentconfig.apps.openshift.io/logging-kibana kibana=openshift/origin-logging-kibana5
oc delete po logging-kibana-1-deploy
