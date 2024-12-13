=== Classification Results ===

Features used in classification:
- fpn

Best parameters: {'C': 2.0, 'gamma': 'scale', 'kernel': 'linear'}

Metrics:
LOOCV Accuracy: 0.842
Precision: 0.800
Recall: 0.889
F1 Score: 0.842
95% Confidence Interval: [0.726, 0.958]

Confusion Matrix:
          Predicted HC  Predicted MDD
True HC             16              4
True MDD             2             16

Detailed Classification Report:
              precision    recall  f1-score   support

          HC       0.89      0.80      0.84        20
         MDD       0.80      0.89      0.84        18

    accuracy                           0.84        38
   macro avg       0.84      0.84      0.84        38
weighted avg       0.85      0.84      0.84        38


Features used in classification:
- fpn

LOOCV Accuracy with best parameters: 0.842

Feature Importance with best parameters:
fpn: 1.660805

Correct predictions: 32 out of 38

Correctly classified subjects:
sub-003P: True group = MDD
sub-005P: True group = MDD
sub-007P: True group = MDD
sub-008P: True group = MDD
sub-009C: True group = HC
sub-010P: True group = MDD
sub-013C: True group = HC
sub-014C: True group = HC
sub-014P: True group = MDD
sub-015C: True group = HC
sub-016C: True group = HC
sub-017C: True group = HC
sub-018C: True group = HC
sub-019C: True group = HC
sub-020P: True group = MDD
sub-021C: True group = HC
sub-024C: True group = HC
sub-025C: True group = HC
sub-026C: True group = HC
sub-027C: True group = HC
sub-028C: True group = HC
sub-030C: True group = HC
sub-031C: True group = HC
sub-032P: True group = MDD
sub-033P: True group = MDD
sub-037P: True group = MDD
sub-042P: True group = MDD
sub-046P: True group = MDD
sub-052P: True group = MDD
sub-066P: True group = MDD
sub-067P: True group = MDD
sub-075P: True group = MDD

Incorrectly classified subjects:
sub-006C: True group = HC, Predicted as = MDD
sub-007C: True group = HC, Predicted as = MDD
sub-020C: True group = HC, Predicted as = MDD
sub-029C: True group = HC, Predicted as = MDD
sub-031P: True group = MDD, Predicted as = HC
sub-048P: True group = MDD, Predicted as = HC


-- Notes
031P is only correctly classified in the salience regions classification
048P is only correctly classified in the salience regions classification