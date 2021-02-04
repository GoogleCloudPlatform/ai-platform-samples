source /conda/etc/profile.d/conda.sh
conda activate rapids

echo "Running: rapids_xgboost.py $@"
python rapids_xgboost.py $@
