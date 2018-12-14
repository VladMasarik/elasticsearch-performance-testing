# Activate .venv
source $GIT_REPO_BASE_DIR/origin-aggregated-logging/hack/.venv/bin/activate

# Update VM deployment script
mv ./get-machine-run-tests.sh $GIT_REPO_BASE_DIR/origin-aggregated-logging/hack/get-machine-run-tests.sh

# Run VM deployment script
$GIT_REPO_BASE_DIR/origin-aggregated-logging/hack/get-machine-run-tests.sh

rsync -avz ./start/ openshiftdevel:/home/origin/

ssh -n openshiftdevel "bash start/init-vm.sh"

ssh openshiftdevel