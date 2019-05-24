# Elasticseach performance testing for Origin Aggregate Logging

This project tests the performance of Elasticsearch deployed as a part of [Origin Aggregate Logging](https://github.com/openshift/origin-aggregated-logging) component. It automatically synchronizes and deploys pods containing [Rally](https://github.com/elastic/rally). The pods are meant to run user specified tests against the Elasticsearch. Results of those tests can then be viewed in Grafana dashboard, which is also deployed by this tool.

## Before using

Before using this project make sure you meet these requirements:

- Have Docker and Python 3 installed.
- Install the Python dependencies
```
$ pip3 install -r requirements.txt
```
- Have an access to an Openshift cluster and be logged in. Verify by executing:
```
$ oc get nodes
# The output should be a list of nodes.
```
- The Openshift cluster has to have a properly deployed Origin Aggregate Logging component. To verify this, go to Openshift web UI and access the Prometheus web UI. Then, navigate to `Status` and `Targets` tab. Find the Elasticsearch entry, based on the name of the service monitor in the `openshift-logging` project.
- Have an access to a container image repository where the script can upload an image.
- Have a folder containing all the necessary files for the Rally. You can use the demo folder `start/esrally-container/copy/single`.
- Start the script from the root directory of this project. Verify by executing:
```
$ ls start/
bootstrap-container  esrally-container
```

## Quick Start

```
$ python3 py-scripts/perfStackDeploy.py REPOSITORY FOLDER
```
Example:
```
$ python3 py-scripts/perfStackDeploy.py docker.io/vladmasarik/hackfest-dep start/esrally-container/copy/single
```
For more help see:
```
python3 py-scripts/perfStackDeploy.py --help
```


## Architecture



## License

Apache License 2.0