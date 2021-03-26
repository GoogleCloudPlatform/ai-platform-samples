from transformers import (
    AutoConfig,
    AutoModelForSequenceClassification,
    AutoTokenizer,
    DataCollatorWithPadding,
    EvalPrediction,
    HfArgumentParser,
    PretrainedConfig,
    Trainer,
    TrainingArguments,
    default_data_collator,
    set_seed,
    PreTrainedTokenizerFast
)
import numpy as np
from datasets import load_dataset, load_metric
from tqdm import tqdm


datasets = load_dataset("imdb")
batch_size = 16
max_seq_length = 128
model_name_or_path = 'bert-base-cased'

label_list = datasets["train"].unique("label")

tokenizer = AutoTokenizer.from_pretrained(
    model_name_or_path,
    use_fast=True,
)

# Dataset loading repeated here to make this cell idempotent
# Since we are over-writing datasets variable
datasets=load_dataset('imdb')

# TEMP: We can extract this automatically but Unique method of the dataset
# is not reporting the label -1 which shows up in the pre-processing
# Hence the additional -1 term in the dictionary
label_to_id = {
    1:1,
    0:0,
    -1:0
}
def preprocess_function(examples):
        # Tokenize the texts
        args = (
            (examples['text'],)
        )
        result = tokenizer(*args, padding='max_length', max_length=max_seq_length, truncation=True)

        # Map labels to IDs (not necessary for GLUE tasks)
        if label_to_id is not None and "label" in examples:
            result["label"] = [label_to_id[l] for l in examples["label"]]
        return result
datasets = datasets.map(preprocess_function, batched=True, load_from_cache_file=True)

model = AutoModelForSequenceClassification.from_pretrained(
        model_name_or_path,
        num_labels=len(label_list)
    )

args = TrainingArguments(
    evaluation_strategy = "epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=batch_size,
    per_device_eval_batch_size=batch_size,
    num_train_epochs=1,
    weight_decay=0.01,
    output_dir='/tmp/cls'
)

def compute_metrics(p: EvalPrediction):
    preds = p.predictions[0] if isinstance(p.predictions, tuple) else p.predictions
    preds = np.argmax(preds, axis=1)
    return {"accuracy": (preds == p.label_ids).astype(np.float32).mean().item()}

trainer = Trainer(
    model,
    args,
    train_dataset=datasets["train"],
    eval_dataset=datasets["test"],
    data_collator=default_data_collator,
    tokenizer=tokenizer,
    compute_metrics=compute_metrics
)


trainer.train()

trainer.evaluate()
