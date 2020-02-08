#!/bin/bash -v
curl -L https://raw.githubusercontent.com/gclouduniverse/nova-agents/master/utils.sh >> utils.sh
source utils.sh

cd ${JUPYTER_SERVER_ROOT}
[[ -e runningjobs ]] || mkdir runningjobs
cd runningjobs
export jobsdir=${GCS_BUCKET}/.jobs/
gsutil ls $jobsdir > /tmp/jobs.txt
while read jobdir; do
  echo $jobdir
  gsutil ls $jobdir > /tmp/machines.txt
  while read machdir; do
    export machine=${machdir:${#jobdir}:-1}
    echo "machine:$machine"
    if [[ "$machine" == "$(hostname)" ]]; then
      gsutil ls ${machdir}DONE
      if [[ "$?" != "0" ]]; then
        export job=${jobdir:${#jobsdir}:-1}
        echo "job:$job"
        [[ -e $job ]] || mkdir $job
        cd $job
        echo "started:$(date)" > RUNNING
        gsutil cp RUNNING ${machdir}RUNNING
        gsutil cp ${machdir}homedir/* .
        gsutil cp ${machdir}$job.yaml .
        export nb=$(get-yaml-val notebook $job.yaml)
        echo "notebook:$nb"
        export outnb=${nb:0:-6}.output.ipynb
        papermill $nb $outnb
        gsutil cp $outnb ${machdir}${outnb}
        mv RUNNING DONE
        echo "finished:$(date)" >> DONE
        gsutil cp DONE ${machdir}DONE
        gsutil rm ${machdir}RUNNING
       
        readonly INSTANCE_NAME=$(curl http://metadata.google.internal/computeMetadata/v1/instance/name -H "Metadata-Flavor: Google")
        INSTANCE_ZONE="/"$(curl http://metadata.google.internal/computeMetadata/v1/instance/zone -H "Metadata-Flavor: Google")
        INSTANCE_ZONE="${INSTANCE_ZONE##/*/}"
        readonly INSTANCE_PROJECT_NAME=$(curl http://metadata.google.internal/computeMetadata/v1/project/project-id -H "Metadata-Flavor: Google")
        gcloud --quiet compute instances delete "${INSTANCE_NAME}" --zone "${INSTANCE_ZONE}" --project "${INSTANCE_PROJECT_NAME}"

      fi
    fi
  done < /tmp/machines.txt
done < /tmp/jobs.txt

