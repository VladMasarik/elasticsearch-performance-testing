oc project openshift-logging

mkdir secret && cd secret

oc extract secrets/logging-elasticsearch

cd ..

docker build --label rallylabel -t docker.io/rallytag .