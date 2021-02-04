source /conda/etc/profile.d/conda.sh
conda activate rapids

echo "Running: rapids_opt2.py $@"
python rapids_opt2.py $@
