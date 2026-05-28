import os
import sys
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression

# Set up paths to allow clean imports from the root and src directories
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.append(current_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from preprocess import clean_text
from evaluate import compute_metrics, plot_confusion_matrices, plot_precision_recall_comparison

def load_and_preprocess_data(csv_path):
    """
    Loads dataset, handles null values, encodes labels, and cleans message text.
    """
    print(f"Loading dataset from: {csv_path}")
    df = pd.read_csv(csv_path)
    
    # Drop rows with missing values in crucial columns
    df = df.dropna(subset=['label', 'message'])
    
    print("Preprocessing raw text messages...")
    df['clean_message'] = df['message'].apply(clean_text)
    
    # Map text labels to binary integers: ham -> 0, spam -> 1
    df['label_encoded'] = df['label'].map({'ham': 0, 'spam': 1})
    
    return df

def train_and_evaluate(df):
    """
    Performs train/test split, vectorization, training of classifiers, 
    evaluates performance, generates evaluation plots, and selects the best model.
    """
    X = df['clean_message']
    y = df['label_encoded']
    
    # Stratified 80/20 train/test split to maintain class ratio
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"Training instances: {len(X_train)}, Testing instances: {len(X_test)}")
    
    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(max_features=5000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)
    
    # 1. Train Naive Bayes
    print("Training Naive Bayes classifier (MultinomialNB)...")
    nb_model = MultinomialNB(alpha=0.2)
    nb_model.fit(X_train_vec, y_train)
    nb_pred = nb_model.predict(X_test_vec)
    nb_prob = nb_model.predict_proba(X_test_vec)
    nb_metrics = compute_metrics(y_test, nb_pred, nb_prob)
    
    # 2. Train Logistic Regression
    print("Training Logistic Regression classifier...")
    lr_model = LogisticRegression(class_weight='balanced', random_state=42)
    lr_model.fit(X_train_vec, y_train)
    lr_pred = lr_model.predict(X_test_vec)
    lr_prob = lr_model.predict_proba(X_test_vec)
    lr_metrics = compute_metrics(y_test, lr_pred, lr_prob)
    
    # Print metrics table
    print("\n" + "="*40)
    print("         EVALUATION METRICS TABLE")
    print("="*40)
    print(f"{'Metric':<15} | {'Naive Bayes':<11} | {'Logistic Reg':<12}")
    print("-"*40)
    for metric in ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'Log Loss']:
        print(f"{metric:<15} | {nb_metrics[metric]:<11.4f} | {lr_metrics[metric]:<12.4f}")
    print("="*40)
    
    # Generate and save evaluation plots
    plots_dir = os.path.join(parent_dir, "plots")
    print(f"Saving evaluation visualizations to {plots_dir}...")
    plot_confusion_matrices(y_test, nb_pred, lr_pred, os.path.join(plots_dir, "confusion_matrix.png"))
    plot_precision_recall_comparison(nb_metrics, lr_metrics, os.path.join(plots_dir, "precision_recall_comparison.png"))
    
    # Select best model based on F1-Score
    if nb_metrics['F1-Score'] >= lr_metrics['F1-Score']:
        best_model = nb_model
        best_model_name = "Naive Bayes"
        best_metrics = nb_metrics
    else:
        best_model = lr_model
        best_model_name = "Logistic Regression"
        best_metrics = lr_metrics
        
    print(f"\nSelected Model: {best_model_name} (F1-Score: {best_metrics['F1-Score']:.4f})")
    
    return vectorizer, best_model, best_model_name, best_metrics, nb_metrics, lr_metrics, y_test, nb_pred, lr_pred

def save_pipeline(vectorizer, model, model_name, metrics, save_path):
    """
    Saves the fitted vectorizer and model pipeline along with metadata using pickle.
    """
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    payload = {
        'vectorizer': vectorizer,
        'model': model,
        'model_name': model_name,
        'metrics': metrics
    }
    with open(save_path, 'wb') as f:
        pickle.dump(payload, f)
    print(f"Saved best model artifacts to: {save_path}")

def main():
    csv_path = os.path.join(parent_dir, "data", "spam.csv")
    if not os.path.exists(csv_path):
        print(f"Error: Dataset {csv_path} not found. Please run download_dataset.py.")
        sys.exit(1)
        
    df = load_and_preprocess_data(csv_path)
    vectorizer, best_model, best_model_name, best_metrics, _, _, _, _, _ = train_and_evaluate(df)
    
    save_path = os.path.join(parent_dir, "models", "model.pkl")
    save_pipeline(vectorizer, best_model, best_model_name, best_metrics, save_path)

if __name__ == "__main__":
    main()
