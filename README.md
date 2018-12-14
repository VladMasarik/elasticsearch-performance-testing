# How to
`deployscript` deployes a VM on Amazon using .get-machines-script from OAL/hack/ 
`get-mach` is the one I use
Watch out as the script replaces `get-mach` in your `OAL` folder!
Deploy machine
Create secrets
Build image
<<Check if pods are deployed properly>>
After 15 mins:
oc edit deamonset logging; remove image tag
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
--track-path=/start/copy \
--target-hosts=10.128.0.42 \
--pipeline=benchmark-only \
--client-options="use_ssl:true,verify_certs:false,ca_certs:'/secret/admin-ca',client_cert:'/secret/admin-cert',client_key:'/secret/admin-key'"
```

# View prometheus
Add user:
`oc adm policy add-cluster-role-to-user cluster-admin origin`

Change name of openshift-monitoring prometheus route to:
`prometheus-k8s.<Amazon-URL>`

Example:
`prometheus-k8s.ec2-5-24-125-613.compute-1.amazonaws.com`

Add that route name to `/etc/hosts`
Connect using browser. Dont forget `https://`