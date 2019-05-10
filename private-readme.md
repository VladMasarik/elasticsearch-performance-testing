# How to
`deployscript` deployes a VM on Amazon using .get-machines-script from OAL/hack/ 
`get-mach` is the one I use
Watch out as the script replaces `get-mach` in your `OAL` folder!
Deploy machine
Create secrets
Build image
<<Check if pods are deployed properly>>
After 15 mins:
oc edit daemonset logging; remove image tag
oc edit dc kibana; remove image tag
oc edit dc es; remove image tag
oc rollout latest dc es
remove kibana deploy (it removed itself after some time)??
"rollout latest" again?? not sure about this one (rollout is running / 10 mins then it fails)
<<END>>
Now you can run the container:
`docker run --rm -it docker.io/rallytag`
Before running rally:
Change IP in the command to IP of the ES-master pod. `oc get pod -o wide`
Run rally using quick, custom made track
```
esrally \
--track-path=/copy \
--target-hosts=10.128.0.48 \
--pipeline=benchmark-only \
--client-options="use_ssl:true,verify_certs:false,ca_certs:'/secret/admin-ca',client_cert:'/secret/admin-cert',client_key:'/secret/admin-key'"

OR 

esrally \
--track-path=$HOME/copy \
--target-hosts=10.128.0.55 \
--pipeline=benchmark-only \
--client-options="use_ssl:true,verify_certs:false,ca_certs:'$HOME/secret/admin-ca',client_cert:'$HOME/secret/admin-cert',client_key:'$HOME/secret/admin-key'"
```


# How to number 2
deploy cluster
deploy openshift logging
fix openshift logging
fix ES scraping


***start script
Deploy etcd service
Deploy etcd 
deploy grafana and other things

label nodes
count nodes
update esrally job nodes
update bootstrap pod with node

wait for the bootstrap node to complete
delete the bootstrap node

delete and export secrets
rebuild image for rally

deploy IS for esrally

deploy esrally


# Fix large ES limits problem


cat ~/.openshift/auth/kubeadmin-password | oc login -u kubeadmin
cd ~/projects/elasticsearch-performance-testing/
oc project openshift-logging
oc scale deploy cluster-logging-operator --replicas=0
oc get elasticsearch elasticsearch -o yaml > temp
sed -i 's/memory: 16Gi/memory: 4Gi/g' temp
sed -i 's/cpu: "1"/cpu: 400m/g' temp
oc apply -f temp
rm temp
oc delete deploy -l component=elasticsearch

#Fix Prometheus ES scraping
oc get servicemonitor -o yaml > temp
sed -i 's/port: elasticsearch-metrics/port: elasticsearch/g' temp
oc apply -f temp
rm temp


# extract secrets for ES testing
cd /home/vmasarik/projects/elasticsearch-performance-testing/start/esrally-container/secret
rm *

oc extract secret/elasticsearch
cd -


# run data creation, zipping, upload


oc delete po esrally --now
cd notPublic/
python3 label-for-bulk.py > temp
gzip temp
mv temp.gz ../start/esrally-container/copy/multiple/
cd ../start/esrally-container/copy/multiple/
mv temp.gz data-nasa-logs-10all.json.gz
cd ../../../../
docker build -t docker.io/vladmasarik/hackfest-dep ./start/esrally-container
docker push docker.io/vladmasarik/hackfest-dep
oc create -f notPublic/po-rally.yaml


#docker build and push

go build polling.go
mv polling ~/projects/elasticsearch-performance-testing/start/copy

docker build -t docker.io/vladmasarik/hackfest-dep /home/vmasarik/projects/elasticsearch-performance-testing/start/esrally-container
docker push docker.io/vladmasarik/hackfest-dep

oc scale deploy rell --replicas=0
oc scale deploy rell --replicas=1




go build bootstrap.go
mv bootstrap start/bootstrap/copy/

docker build -t docker.io/vladmasarik/hackfest-pod /home/vmasarik/projects/elasticsearch-performance-testing/start/bootstrap
docker push docker.io/vladmasarik/hackfest-pod


# View prometheus
Add user:
`oc adm policy add-cluster-role-to-user cluster-admin origin`

Change name of openshift-monitoring prometheus route to:
`prometheus-k8s.<Amazon-URL>`

Example:
`prometheus-k8s.ec2-5-24-125-613.compute-1.amazonaws.com`

Add that route name to `/etc/hosts`
Connect using browser. Dont forget `https://`

# Regex to parse tha NASA logs:
`:%s:^\([a-zA-Z0-9\.\-\_\@\'\,\&\#\:\*\/]\+\)\s-\s-\s\(\[.\+\]\)\s\(\".\+\"\)\s\([0-9]\+\)\s\([0-9\-]\+\)
:\{\"ip\"\: \"\1\", \"date\"\: \"\2\", \"request\"\: \3, \"result\"\: \4, \"size\"\: \5\},`




# Get uniq node names for pod
oc get po -o custom-columns=NODE:.spec.nodeName --all-namespaces | sort | uniq -c


# Extra index in track.json

,
    {
      "name": "extra-index-nasa-logs",
      "body": "indexTwo.json",
      "types": [ "docs" ]
    }



# po rell in case i want to use preStart
    command: ["sleep", "10000000"]
    lifecycle:
      postStart:
        httpGet:
          host: <host-placeholder>
          path: "/v2/keys/"
          port: 2379



    lifecycle:
      postStart:
        exec:
          command: ["/bin/sh", "-c", "/home/rell/copy/qqqqq"]



# Curl prometheus
curl -k --header "Authorization: Bearer `cat /var/run/secrets/kubernetes.io/serviceaccount/token`" https://elasticsearch-metrics.openshift-logging.svc.cluster.local:60000/_prometheus/metrics





# Incase you cannot get through Grafana login. Add
`-skip-provider-button=true` to the grafana deployment

# Download then start testing
I guess i need to start from the container, meaning get all really and after the container is running start downloading the data. Check if other containers are ready too and if they are run it. With my own data i will just provide from where to get it. For esrally data I will get the download thing but not sure if I need it.

# Grafana set up
Postup pri nastaveni grafany.


New deployment copied from monitoring. deleted all not needed volumes except for the defined by me + i had to leave some basic/simple named volume grafana-volume or so.

new service pointing to new grafana
new route pointing to new service. route had changed tls names, also in deployment? but still does not work. BUT if i change the starting route "grafana" to redirect to modified service it will be working. it should be changed by operator, but so far it did not.

new config map that contains the grafana dashboards


question: Where is te grafana getting the data from? prometheus?


# How to fix Prometheus scraping and add dashboard to grafana
- openshift
have openshift-dev account on Amazon
Get a pull secret from 4th step ( https://cloud.openshift.com/clusters/install OR https://try.openshift.com/ ==> sign in)
openshift-install --dir=<DIR where to put install config> create install-config
    select us-east-1
    devcluster
    your name
    pull secret
openshift-install --log-level=debug --dir=<DIR with install config> create cluster
- logging
dont forget to set KUBECONFIG and other env var
go into GO directory ==> cluster logging ==> run
REMOTE_CLUSTER=true make undeploy
REMOTE_CLUSTER=true make deploy-example-no-build




<<<<This one should not be needed anymore>>>>

- fix scraping
- edit ES service by adding name
oc project openshift-logging 
oc get service elasticsearch -o yaml > serviceyaml
sed -i 's/- port:/- name: restapi\n    port:/g' serviceyaml
oc apply -f serviceyaml
rm serviceyaml

  


edit service monitor by disabling auth and add serverName: <name of service>
    tlsConfig:
      caFile: /etc/prometheus/configmaps/serving-certs-ca-bundle/service-ca.crt
      insecureSkipVerify: true -add
      serverName: elasticsearch -add

oc get servicemonitor monitor-elasticsearch-cluster -o yaml > smyaml
sed -i 's/ca.crt/ca.crt\n      insecureSkipVerify: true\n      serverName: elasticsearch/g' smyaml

oc apply -f smyaml
<<<<This one should not be needed anymore>>>>

# Dashboard setup
check if it works on prometheus by going into UI console (URL at the end of openshift-install) and monitoring
- set up grafana
create config map with your dashboard


oc project openshift-monitoring
oc create -f cm-dashboard-logging

create modified grafana with removed etcd and added your config map (both volume things)

oc create -f dep-grafana


create service for grafana
oc create -f svc-grafana

point defualt route onto modified service

oc patch route grafana -p '{"spec":{"to":{"name":"grafana-logging"}}}'


- start testing
create a job and run it
oc create -f dep
wait
- watch logs
console GUI ==> monitoring
- kill cluster
openshift-install destroy cluster --dir=<DIR with install config> --log-level debug



# Check ES if API is open
curl -k --header "Authorization: Bearer `cat /var/run/secrets/kubernetes.io/serviceaccount/token`" https://elasticsearch.openshift-logging.svc.cluster.local:9200/_prometheus/metrics