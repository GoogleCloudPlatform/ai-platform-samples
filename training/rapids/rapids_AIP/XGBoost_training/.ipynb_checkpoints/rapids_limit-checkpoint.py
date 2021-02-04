from dask_cuda import LocalCUDACluster
from dask.distributed import Client, wait
from dask import array as da
import xgboost as xgb
from xgboost import dask as dxgb
from xgboost.dask import DaskDMatrix
from dask.utils import parse_bytes
import cupy as cp
import argparse
import time
import gcsfs
import dask_cudf
import os, json
import subprocess


def using_quantile_device_dmatrix(client: Client, train_dir, model_file, fs, do_wait=False):
    '''`DaskDeviceQuantileDMatrix` is a data type specialized for `gpu_hist`, tree
     method that reduces memory overhead.  When training on GPU pipeline, it's
     preferred over `DaskDMatrix`.
    .. versionadded:: 1.2.0
    '''
    colnames = ['label'] + ['feature-%02d' % i for i in range(1, 29)]
    df = dask_cudf.read_csv(train_dir, header=None, names=colnames, chunksize=None)
    X = df[df.columns.difference(['label'])]
    y = df['label']
    print("[INFO]: ------ CSV files are read from" + train_dir)
   

    if do_wait is True:
        df = df.persist()
        X = X.persist()
        wait(df)
        wait(X)
        print("[INFO]: ------ Long waited but the data is ready now")
    

    # `DaskDeviceQuantileDMatrix` is used instead of `DaskDMatrix`, be careful
    # that it can not be used for anything else than training.
    start_time = time.time()
    dtrain = dxgb.DaskDeviceQuantileDMatrix(client, X, y)
    print("[INFO]: ------ QuantileDMatrix is formed in {} seconds ---".format((time.time() - start_time)))
   
    del df
    del X
    del y

    start_time = time.time()
    output = xgb.dask.train(client,
                        { 'verbosity': 2,
                         'learning_rate': 0.1,
                          'max_depth': 8,
                          'objective': 'reg:squarederror',
                          'subsample': 0.5,
                          'gamma': 0.9,
                          'verbose_eval': True,
                          'tree_method':'gpu_hist',
                          #'nthread':1
                        },
                        dtrain,
                        num_boost_round=100, evals=[(dtrain, 'train')])
    print("[INFO]: ------ Training is completed in {} seconds ---".format((time.time() - start_time)))
    
    history = output['history']
    print('[INFO]: ------ Training evaluation history:', history)
    
    output['booster'].save_model('/tmp/tmp.model')
    fs.put('/tmp/tmp.model', model_file)
    print("[INFO]: ------ Model saved here:{}".format( model_file))

def get_scheduler_info():
    scheduler_ip =  subprocess.check_output(['hostname','--all-ip-addresses'])
    scheduler_ip = scheduler_ip.decode('UTF-8').split()[0]
    scheduler_port = '8786'
    scheduler_uri = '{}:{}'.format(scheduler_ip, scheduler_port)
    return scheduler_ip, scheduler_uri



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--gcp-project', type=str, help='user gcp project',
        default='crisp-sa')
    parser.add_argument(
        '--train-files', type=str, help='Training files local or GCS',
        default='gs://crisp-sa/rapids/higgs_csv/*.csv')
    parser.add_argument(
        '--model-file', type=str,
        help="""GCS or local dir for checkpoints, exports, and summaries.
        Use an existing directory to load a trained model, or a new directory
        to retrain""",
        default='gs://crisp-sa/rapids/models/001.model')
    parser.add_argument(
        '--num-gpu-per-worker', type=int, help='num of workers',
        default=2)
    parser.add_argument(
        '--threads-per-worker', type=int, help='num of threads per worker',
        default=4)
    parser.add_argument(
        '--do-wait', action='store_true', help='do persist/wait data')

    args = parser.parse_args()

    print("[INFO]: ------ Arguments parsed")
    print(args)

    
    fs = gcsfs.GCSFileSystem(project=args.gcp_project, token='cloud')
    print("[INFO]: ------ gcsfs object is created")

    sched_ip, sched_uri = get_scheduler_info()
    

    print("[INFO]: ------ LocalCUDACluster is being formed with device memory limit 13gb")
    # `LocalCUDACluster` is used for assigning GPU to XGBoost processes.  Here
    # `n_workers` represents the number of GPUs since we use one GPU per worker
    # process.
    with LocalCUDACluster(ip=sched_ip, 
                          n_workers=args.num_gpu_per_worker, 
                          threads_per_worker=args.threads_per_worker, 
                          rmm_pool_size=parse_bytes("13GB"),
                          device_memory_limit=parse_bytes("13GB")) as cluster:
    #with LocalCUDACluster(n_workers=args.num_gpu_per_worker, threads_per_worker=args.threads_per_worker) as cluster:
        with Client(cluster) as client:
            # generate some random data for demonstration

            print('[INFO]: ------ Calling main function ')
            using_quantile_device_dmatrix(client, args.train_files, args.model_file, fs, args.do_wait)
 '''         
    with LocalCUDACluster(ip=sched_ip, n_workers=args.num_gpu_per_worker, threads_per_worker=args.threads_per_worker, device_memory_limit=parse_bytes("13GB")) as cluster:
    #with LocalCUDACluster(n_workers=args.num_gpu_per_worker, threads_per_worker=args.threads_per_worker) as cluster:
        with Client(cluster) as client:
            # generate some random data for demonstration

            print('[INFO]: ------ Calling main function')
            using_quantile_device_dmatrix(client, args.train_files, args.model_file, fs, args.do_wait)
'''