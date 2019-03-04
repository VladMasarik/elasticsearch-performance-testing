# Activate .venv
source $GIT_REPO_BASE_DIR/origin-aggregated-logging/hack/.venv/bin/activate

# Update VM deployment script
mv ./get-machine-run-tests.sh $GIT_REPO_BASE_DIR/origin-aggregated-logging/hack/get-machine-run-tests.sh

# Run VM deployment script
$GIT_REPO_BASE_DIR/origin-aggregated-logging/hack/get-machine-run-tests.sh

rsync -avz $GIT_REPO_BASE_DIR/elasticsearch-performance-testing/start/ openshiftdevel:/data/src/start/

ssh -n openshiftdevel "bash /data/src/start/init-vm.sh"

ssh openshiftdevel

