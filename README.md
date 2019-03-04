## Project for ES performance testing
# How to
It is expected that you have running OpenShift cluster using `openshift-installer`, and that you have deployed `cluster-logging` using `cluster-logging-operator`
Now you need to:
create secrets and create your own container
create imagestream
label all the nodes that dont have ES
deploy rally on those labeled nodes
view the data after testing