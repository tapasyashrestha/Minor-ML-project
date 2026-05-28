import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, log_loss, confusion_matrix
)

def compute_metrics(y_true, y_pred, y_prob):
    """
    Computes Accuracy, Precision, Recall, F1-Score, and Log Loss for binary classification.
    
    Parameters:
    y_true (array-like): True binary labels (0 for ham, 1 for spam).
    y_pred (array-like): Predicted binary labels.
    y_prob (array-like): Predicted probabilities (2D array of shape [n_samples, 2]).
    
    Returns:
    dict: Dictionary containing the calculated metrics.
    """
    return {
        'Accuracy': float(accuracy_score(y_true, y_pred)),
        'Precision': float(precision_score(y_true, y_pred, zero_division=0)),
        'Recall': float(recall_score(y_true, y_pred, zero_division=0)),
        'F1-Score': float(f1_score(y_true, y_pred, zero_division=0)),
        'Log Loss': float(log_loss(y_true, y_prob))
    }

def plot_confusion_matrices(y_true, nb_pred, lr_pred, save_path):
    """
    Generates and saves a side-by-side confusion matrix plot for Naive Bayes and Logistic Regression.
    
    Parameters:
    y_true (array-like): True labels.
    nb_pred (array-like): Naive Bayes predictions.
    lr_pred (array-like): Logistic Regression predictions.
    save_path (str): File path to save the generated plot.
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    
    # Naive Bayes Confusion Matrix
    cm_nb = confusion_matrix(y_true, nb_pred)
    sns.heatmap(cm_nb, annot=True, fmt='d', cmap='Blues', ax=axes[0],
                xticklabels=['Ham', 'Spam'], yticklabels=['Ham', 'Spam'])
    axes[0].set_title('Naive Bayes Confusion Matrix', fontsize=14, pad=10)
    axes[0].set_xlabel('Predicted Label', fontsize=12)
    axes[0].set_ylabel('True Label', fontsize=12)
    
    # Logistic Regression Confusion Matrix
    cm_lr = confusion_matrix(y_true, lr_pred)
    sns.heatmap(cm_lr, annot=True, fmt='d', cmap='Greens', ax=axes[1],
                xticklabels=['Ham', 'Spam'], yticklabels=['Ham', 'Spam'])
    axes[1].set_title('Logistic Regression Confusion Matrix', fontsize=14, pad=10)
    axes[1].set_xlabel('Predicted Label', fontsize=12)
    axes[1].set_ylabel('True Label', fontsize=12)
    
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_precision_recall_comparison(nb_metrics, lr_metrics, save_path):
    """
    Generates and saves a bar chart comparing performance metrics across models.
    
    Parameters:
    nb_metrics (dict): Metrics dictionary for Naive Bayes.
    lr_metrics (dict): Metrics dictionary for Logistic Regression.
    save_path (str): File path to save the comparison plot.
    """
    metrics_to_plot = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
    
    data = {
        'Metric': metrics_to_plot * 2,
        'Value': [nb_metrics[m] for m in metrics_to_plot] + [lr_metrics[m] for m in metrics_to_plot],
        'Model': ['Naive Bayes'] * 4 + ['Logistic Regression'] * 4
    }
    
    df = pd.DataFrame(data)
    
    plt.figure(figsize=(10, 6))
    # Elegant color palette
    sns.barplot(x='Metric', y='Value', hue='Model', data=df, palette=['#3182bd', '#31a354'])
    plt.title('Classifier Performance Comparison', fontsize=16, pad=15)
    plt.ylabel('Metric Score', fontsize=12)
    plt.xlabel('Metric', fontsize=12)
    plt.ylim(0, 1.1)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Annotate metrics values on the bars
    ax = plt.gca()
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f'{height:.3f}',
                        (p.get_x() + p.get_width() / 2., height),
                        ha='center', va='bottom', fontsize=10, xytext=(0, 5),
                        textcoords='offset points', weight='bold')
            
    plt.legend(loc='lower right', frameon=True, shadow=True)
    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
