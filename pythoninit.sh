
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
