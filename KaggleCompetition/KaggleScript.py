# roberta_author_classifier.py

import os
# Disable Weights & Biases to avoid hanging
os.environ["WANDB_DISABLED"] = "true"
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import torch
from datasets import Dataset
from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
)

def main():
    # Paths
    TRAIN_PATH = "/kaggle/input/identify-the-author/train/train.csv"
    TEST_PATH  = "/kaggle/input/identify-the-author/test/test.csv"
    OUT_PATH   = "/kaggle/working/submission.csv"

    # Load training data
    # Expect columns: id, text, author
    df = pd.read_csv(TRAIN_PATH)
    label2id = {"EAP": 0, "HPL": 1, "MWS": 2}
    id2label = {v: k for k, v in label2id.items()}
    df["label"] = df["author"].map(label2id)

    # Split into train/validation
    train_df, val_df = train_test_split(
        df, test_size=0.1, stratify=df["label"], random_state=42
    )

    # Create 🤗 Datasets
    train_ds = Dataset.from_pandas(train_df[["text", "label"]])
    val_ds   = Dataset.from_pandas(val_df[["text", "label"]])

    # Tokenizer
    tokenizer = AutoTokenizer.from_pretrained("roberta-base")
    def tokenize(batch):
        return tokenizer(
            batch["text"],
            padding="max_length",
            truncation=True,
            max_length=256,
        )

    print("Tokenizing training set...")
    train_ds = train_ds.map(tokenize, batched=True)
    print("Tokenizing validation set...")
    val_ds   = val_ds.map(tokenize, batched=True)
    train_ds.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])
    val_ds.set_format(type="torch", columns=["input_ids", "attention_mask", "label"])

    # Model
    model = AutoModelForSequenceClassification.from_pretrained(
        "roberta-base", num_labels=3, id2label=id2label, label2id=label2id
    )

    # Metrics
    def compute_metrics(eval_pred):
        logits, labels = eval_pred
        preds = np.argmax(logits, axis=1)
        return {"accuracy": accuracy_score(labels, preds)}

    # Training arguments (legacy API)
    training_args = TrainingArguments(
        output_dir="roberta-author",
        report_to="none",         # disable W&B
        do_train=True,
        do_eval=True,
        logging_dir="logs",
        logging_steps=10,           # more frequent logs
        eval_steps=500,
        save_steps=500,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=32,
        learning_rate=2e-5,
        num_train_epochs=3,        # tried it with 5 epochs, but it overfitted
        weight_decay=0.01,
        fp16=True,                  # mixed precision if supported
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=val_ds,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )

    # Fine-tune
    print("Starting training...")
    trainer.train()
    print("Training complete")

    # Inference on test set
    print("Tokenizing test set and running inference...")
    test_df = pd.read_csv(TEST_PATH)
    test_ds = Dataset.from_pandas(test_df[["text"]])
    test_ds = test_ds.map(tokenize, batched=True)
    test_ds.set_format(type="torch", columns=["input_ids", "attention_mask"])

    preds = trainer.predict(test_ds)
    probs = torch.softmax(torch.from_numpy(preds.predictions), dim=-1).numpy()

    # Prepare submission
    submission = pd.DataFrame({
        "id":  test_df["id"],
        "EAP": probs[:, label2id["EAP"]],
        "HPL": probs[:, label2id["HPL"]],
        "MWS": probs[:, label2id["MWS"]],
    })
    submission.to_csv(OUT_PATH, index=False)
    print("Wrote submission to:", OUT_PATH)

if __name__ == "__main__":
    main()
