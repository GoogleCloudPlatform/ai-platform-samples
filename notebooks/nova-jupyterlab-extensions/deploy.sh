INSTANCE_NAME=$1

gcloud compute ssh "jupyter@${INSTANCE_NAME}" -- "sudo rm -rf /home/jupyter/nova"
gcloud compute ssh "jupyter@${INSTANCE_NAME}" -- "mkdir -p /home/jupyter/nova"
gcloud compute scp --recurse ./* "jupyter@${INSTANCE_NAME}:/home/jupyter/nova"
gcloud compute ssh "jupyter@${INSTANCE_NAME}" -- "sudo pip3 uninstall -y jupyterlab-nova"
gcloud compute ssh "jupyter@${INSTANCE_NAME}" -- "sudo pip3 install /home/jupyter/nova"
gcloud compute ssh "jupyter@${INSTANCE_NAME}" -- "sudo service jupyter restart"
gcloud compute ssh "jupyter@${INSTANCE_NAME}" -- "cd /home/jupyter/nova && sudo jupyter labextension install"
