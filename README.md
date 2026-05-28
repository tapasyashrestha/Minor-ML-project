# 📧 Intelligent SMS Spam Detector

An end-to-end Machine Learning project that classifies SMS messages as **Spam** or **Ham (Legitimate)** using Natural Language Processing (NLP), Scikit-Learn classifiers, and a premium interactive Streamlit web interface.

---

## 🚀 Live Demo & Streamlit Web Interface

The project includes an interactive web application built with Streamlit. It allows users to input any custom SMS message, view classification results, see predicted probabilities, and inspect how the text is preprocessed under the hood.

### Launching the Application
```bash
streamlit run app.py
```

---

## 📊 Model Performance Results

We trained and compared two classifiers on the SMS Spam Collection dataset: **Naive Bayes (MultinomialNB)** and **Logistic Regression**. The results below are evaluated on the held-out test set (20% stratified split).

| Classifier | Accuracy | Precision | Recall | F1-Score | Log Loss |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Logistic Regression** | **98.12%** | 93.84% | **91.95%** | **0.9288** | 0.1495 |
| **Naive Bayes (alpha=0.2)** | **98.12%** | **98.48%** | 87.25% | 0.9253 | **0.0686** |

*Note: Logistic Regression (balanced class weights) was selected as the final production model due to its superior F1-Score (0.9288) and high Recall (91.95%), ensuring fewer spam messages slip through undetected.*

---

## 🧠 Machine Learning Concepts Covered

This repository serves as an educational portfolio project covering core concepts in classification and NLP:

- **Supervised Learning**: Binary classification on labeled text data.
- **Train/Test Split**: 80/20 stratified split to handle class imbalance.
- **Text Preprocessing**: Lowercasing, punctuation/special characters removal, stopword filtering, and Porter Stemming.
- **Feature Extraction (TF-IDF)**: Vectorizing raw text into normalized numerical feature representations.
- **Classifiers**: Naive Bayes (probabilistic) vs. Logistic Regression (linear classification).
- **Evaluation Metrics**: Why F1-Score, Precision, and Recall are superior to Accuracy alone on imbalanced datasets.
- **Bias-Variance Tradeoff**: Analyzing how MultinomialNB's independence assumption (high bias) compares with Logistic Regression.
- **Log Loss / Cross-Entropy**: Used to evaluate predicted probabilities.

---

## 📁 Folder Structure

```
📁 Minor-ML-project/
│
├── 📁 data/
│   └── spam.csv                    ← Processed SMS dataset (5,572 rows)
│
├── 📁 notebooks/
│   ├── 01_EDA.ipynb                ← Exploratory data analysis, distributions, and word clouds
│   ├── 02_preprocessing.ipynb      ← NLP text cleaning and TF-IDF step-by-step walk-through
│   └── 03_model_training.ipynb     ← Classifier training, evaluations, and hyperparameter tuning
│
├── 📁 src/
│   ├── preprocess.py               ← Reusable NLP text cleaning pipeline module
│   ├── train.py                    ← Standalone model training and serialization pipeline
│   └── evaluate.py                 ← Visualizations and performance metrics helper module
│
├── 📁 models/
│   └── model.pkl                   ← Serialized production vectorizer and classifier pipeline
│
├── 📁 plots/
│   ├── class_distribution.png      ← Bar chart of target distribution
│   ├── length_distribution.png     ← Message character length distribution
│   ├── wordcloud_spam.png          ← Word cloud of spam words
│   ├── wordcloud_ham.png           ← Word cloud of ham words
│   ├── top_20_spam_words.png       ← Top 20 terms in spam messages
│   ├── confusion_matrix.png        ← Confusion matrices for NB & LR
│   └── precision_recall_comparison.png ← Metrics bar chart comparison
│
├── app.py                          ← Streamlit web application
├── requirements.txt                ← Project package requirements
├── .gitignore                      ← Excludes virtual environments and Python cache
└── README.md                       ← Project documentation (this file)
```

---

## ⚙️ Installation & Usage

### 1. Clone the repository and navigate to the project directory
```bash
git clone https://github.com/yourusername/Minor-ML-project.git
cd Minor-ML-project
```

### 2. Set up virtual environment and install dependencies
```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment (Windows)
.venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 3. Run Notebooks
You can open and execute the notebooks step-by-step using Jupyter:
```bash
jupyter notebook
```
Or run them programmatically in one command:
```bash
jupyter nbconvert --to notebook --execute --inplace notebooks/*.ipynb
```

### 4. Train the Model
The model is pre-trained and saved under `models/model.pkl`. To retrain the model and regenerate all plots, run:
```bash
python src/train.py
```

### 5. Launch the Streamlit Web App
To check custom SMS messages on the web interface, execute:
```bash
streamlit run app.py
```

---

## 📜 Dataset Reference
The dataset used in this project is the **SMS Spam Collection Dataset** from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/SMS+Spam+Collection). It comprises 5,572 English, non-encoded, real-world SMS messages tagged as legitimate (ham) or spam.

---

## 📄 License
This project is open-source and licensed under the [MIT License](LICENSE).