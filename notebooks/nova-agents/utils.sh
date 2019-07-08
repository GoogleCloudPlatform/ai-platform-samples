export JUPYTER_HOME=/home/jupyter
export GCS_BUCKET=gs://nova-artifacts-$(gcloud config get-value project)
export ZONE=$(gcloud config get-value compute/zone)
if [[ $ZONE == "" ]]; then
  export ZONE=$(curl http://metadata.google.internal/computeMetadata/v1/instance/zone -H "Metadata-Flavor: Google")
  export ZONE="${ZONE##*/}"
fi

function get-yaml-val() {
  export key=$1:
  export val=$(grep ${key} $2)
  echo ${val:${#key}:${#val}}
}

function get-image() {
  hostname | grep -q pytorch
  if [[ "$?" == "0" ]]; then
    echo pytorch-latest-gpu
  else
    echo tf-latest-gpu
  fi
}

function get-accelerator-options() {
  if [[ "$1" == "0" ]]; then
    echo ""
  else
    echo "--accelerator=type=$2,count=$1"
  fi
}
