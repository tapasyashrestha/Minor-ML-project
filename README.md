# SMS Spam Detector

A beginner ML project that classifies SMS messages as **Spam** or **Ham (Legitimate)**.  
Built to learn text classification, TF-IDF vectorization, and model evaluation on imbalanced data.

---

## What this project does

Takes a raw SMS message → cleans the text → converts it to numbers using TF-IDF → runs it through a trained classifier → outputs **Spam** or **Ham** with a confidence score.

Two classifiers were trained and compared: **Naive Bayes** and **Logistic Regression**.

---

## Results

Both models hit 98% accuracy — but accuracy is misleading here because 87% of messages are already Ham. So I focused on F1-Score and Recall instead.

| Classifier | Accuracy | Precision | Recall | F1-Score | Log Loss |
|---|---|---|---|---|---|
| Logistic Regression | 98.12% | 93.84% | 91.95% | 0.9288 | 0.1495 |
| Naive Bayes (alpha=0.2) | 98.12% | 98.48% | 87.25% | 0.9253 | 0.0686 |

**Final model: Logistic Regression** — it had better Recall (91.95% vs 87.25%), meaning it catches more actual spam messages. Missing a spam is worse than a false alarm, so Recall mattered more here.

This was also the first time I really understood why accuracy alone is a bad metric on imbalanced datasets.

---

## What I learned

- Why F1-Score and Recall matter more than Accuracy on imbalanced data
- How TF-IDF converts raw text into numbers a model can actually use
- The difference between how Naive Bayes and Logistic Regression think about the problem
- How `class_weight='balanced'` helps Logistic Regression handle the 87/13 class split
- What Log Loss actually measures and why lower is better

---

## Folder Structure

```
📁 Minor-ML-project/
│
├── 📁 data/
│   └── spam.csv
│
├── 📁 notebooks/
│   ├── 01_EDA.ipynb               ← data exploration, class imbalance, word distributions
│   ├── 02_preprocessing.ipynb     ← text cleaning + TF-IDF walkthrough
│   └── 03_model_training.ipynb    ← training, evaluation, hyperparameter tuning
│
├── 📁 src/
│   ├── preprocess.py              ← text cleaning functions
│   ├── train.py                   ← trains and saves the model
│   └── evaluate.py                ← metrics and plots
│
├── 📁 models/
│   └── model.pkl                  ← saved model (so you don't have to retrain)
│
├── 📁 plots/
│   ├── class_distribution.png
│   ├── length_distribution.png
│   ├── top_20_spam_words.png
│   ├── confusion_matrix.png
│   └── precision_recall_comparison.png
│
├── app.py                         ← Streamlit app
├── requirements.txt
└── README.md
```

---

## How to run it

**1. Clone and set up**
```bash
git clone https://github.com/yourusername/Minor-ML-project.git
cd Minor-ML-project
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

**2. Run the notebooks** (in order — 01 → 02 → 03)
```bash
jupyter notebook
```

**3. Retrain the model** (optional — model.pkl is already included)
```bash
python src/train.py
```

**4. Launch the web app**
```bash
streamlit run app.py
```

---

## Dataset

[SMS Spam Collection — UCI ML Repository](https://archive.ics.uci.edu/ml/datasets/SMS+Spam+Collection)  
5,572 real SMS messages labeled as spam or ham.

---

## Tech Stack

| Library | Used for |
|---|---|
| pandas | loading and exploring the data |
| numpy | numerical operations |
| matplotlib / seaborn | all visualizations |
| scikit-learn | TF-IDF, models, metrics |
| pickle | saving and loading the model |
| streamlit | web app |

---

## What I'd improve next time

- Try CountVectorizer vs TF-IDF and compare the results
- Add bigrams/trigrams to capture phrases like "free offer"
- Test Random Forest and SVM on the same data
- Add NLTK stopword removal and stemming for cleaner features

---

*Part of my ML learning journey. Dataset is publicly available under open license.*
