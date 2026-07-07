# Credit Card Fraud Detection

This project detects fraudulent credit card transactions. Instead of building one model and stopping there, it compares three things: a supervised model, an unsupervised model, and a real cost comparison between the two. The goal was to actually understand which approach works better and by how much, not just report one accuracy number.

## Dataset

The dataset contains European cardholder transactions from September 2013. It has 284,807 transactions total, and only 492 of them are fraud, which is 0.172% of the data. Most of the columns (V1 through V28) are the result of a PCA transformation done to protect user privacy, so their original meaning is hidden. Only `Time` and `Amount` are left in their original, readable form.

The raw dataset file is not included in this repo because it is too large for GitHub. You can download it from Kaggle here: [ULB Credit Card Fraud dataset](https://www.kaggle.com/mlg-ulb/creditcardfraud). Once downloaded, place the CSV file inside `data/raw/`.

## Why this project is structured this way

Most fraud detection projects online use accuracy as the main metric, but accuracy is misleading here. A model that just guesses "not fraud" every single time would still be 99.8% accurate while catching zero actual fraud. So this project avoids that trap in three ways:

1. Uses a supervised model that handles the imbalance properly, and judges it using AUPRC instead of accuracy.
2. Builds a second, unsupervised model to see what happens when fraud labels are not available yet, which is a realistic situation in real fraud systems.
3. Converts both models' results into actual dollar cost, so the comparison means something in plain business terms, not just abstract percentages.

## Project structure

```
project/
├── data/
│   ├── raw/                    place creditcard.csv here, not tracked in git
│   └── processed/              train and test split, created by 01_eda.ipynb
├── notebook/
│   ├── 01_eda.ipynb
│   ├── 02_supervised_model.ipynb
│   ├── 03_anomaly_detection.ipynb
│   └── 04_cost_sensitive_eval.ipynb
├── src/
│   └── utils.py                 shared cost calculation function
├── artifacts/                   saved trained models, not tracked in git
├── requirements.txt
└── README.md
```

## What each notebook does and what it found

**01_eda.ipynb**
Explored the raw data before any modeling. Confirmed the severe imbalance (0.172% fraud), found and removed 1,081 duplicate rows (19 of which were fraud cases), and identified which features (V14, V17, V12, V10, V11, V4) show the clearest difference between fraud and genuine transactions. Created one fixed train and test split, saved to disk, so every later notebook uses the exact same data and results stay comparable.

**02_supervised_model.ipynb**
Trained an XGBoost model, using a technique called `scale_pos_weight` to handle the class imbalance instead of generating fake synthetic data through SMOTE. Result: AUPRC of 0.8139, which is a strong score for this problem. At the standard decision threshold, it correctly catches 75 out of 95 fraud cases while wrongly flagging only 7 genuine transactions. One interesting finding: the feature with the strongest simple correlation to fraud (V17) was not the most important feature to the actual model. V14 turned out to matter far more, and this was investigated and confirmed to not be a case of overlapping features.

**03_anomaly_detection.ipynb**
Trained an Isolation Forest model, which never sees the fraud labels during training. It only learns what a normal transaction looks like and flags anything unusual. Result: AUPRC of 0.1040, far lower than the supervised model. This is not a failed experiment, it is the expected outcome. It shows clearly, with real numbers, why having labeled fraud data available makes such a large difference, and it represents a fallback approach for situations where labels are not yet available.

**04_cost_sensitive_eval.ipynb**
Took both trained models and calculated what they would actually cost in dollars if used in the real world. A missed fraud case is costed at the real transaction amount lost. A false alarm is costed at a flat 10 dollar review fee, representing the staff time needed to check a flagged transaction. Under this cost model, the XGBoost model's total cost was $4,624.05, while the Isolation Forest model's total cost was $13,976.32. That means choosing the wrong model here would have cost about $9,352 more on this same set of transactions. Almost this entire gap comes from missed fraud value, not from false alarms. The $10 review cost is an assumption used to make the comparison possible, not a confirmed real world number, but the overall result (XGBoost being much cheaper) holds true regardless of the exact review cost used.

## Setup instructions

```bash
conda create -p venv python=3.11
conda activate venv/
pip install -r requirements.txt
```

Then open the notebooks in order, starting with `01_eda.ipynb`, since each one depends on files created by the notebook before it.

## Status

All four notebooks are complete.