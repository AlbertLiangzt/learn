print(__doc__)

import sys
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, precision_recall_curve

inputfile = sys.argv[1]

label_list = []
score_list = []
with open(inputfile, 'r') as fd:
    for line in fd:
        fs = line.strip().split('	')
        label = int(fs[0])
        score = float(fs[1])
        label_list.append(label)
        score_list.append(score)

fpr, tpr, _ = roc_curve(label_list, score_list)
auc = auc(fpr, tpr)

precision, recall, _ = precision_recall_curve(label_list, score_list)

##############################################################################
# Plot of a ROC curve for a specific class
plt.figure()
plt.plot(fpr, tpr)
plt.plot([0, 1], [0, 1], 'k--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC curve (auc = %.2f)' % auc)
plt.legend(loc="lower right")
plt.show()

plt.figure()
plt.plot(recall, precision)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('recall')
plt.ylabel('precision')
plt.title('Precision-Recall curve')
plt.legend(loc="lower right")
plt.show()
