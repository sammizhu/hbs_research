import pandas as pd
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt
import numpy as np

# Load your dataset
data = pd.read_csv('')

true_labels = data['deepface_race']

# Define a range of weights to test
weights = np.linspace(0, 1, 101)  # From 0 to 1 in steps of 0.01
best_auc = 0
best_weight = None

for weight in weights:
    # Combined probability calculation
    combined_prob = weight * data['deepface_race'] + (1 - weight) * data['ethnicolr_race']
    
    # Calculate ROC curve and AUC
    fpr, tpr, _ = roc_curve(true_labels, combined_prob)
    roc_auc = auc(fpr, tpr)
    
    # Plot ROC curve for each weight
    plt.plot(fpr, tpr, lw=1, alpha=0.3, label=f'ROC (weight={weight:.2f}, AUC={roc_auc:.2f})' if roc_auc > best_auc else "")

    # Track the best AUC and corresponding weight
    if roc_auc > best_auc:
        best_auc = roc_auc
        best_weight = weight

# Plotting the best ROC curve
plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='navy', label='Chance')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right", fontsize='small')
plt.show()

print("Best Weight:", best_weight)
print("Best AUC:", best_auc)
