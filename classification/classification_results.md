# Classification results

## Initial Classification
This initial classification was done using only the unimodal regions as features. This follows the principle of parsimony in feature selection.

### Features: Unimodal regions (auditory, visual, motor)
```
Best parameters: {'C': 0.5, 'gamma': 'scale', 'kernel': 'linear'}
Best cross-validation accuracy: 0.5789473684210527

Features used in classification:
- visual
- motor
- auditory

LOOCV Accuracy with best parameters: 0.579
95% Confidence Interval: [0.422, 0.736]

Correct predictions: 22 out of 38

Correctly classified subjects:
sub-006C: True group = HC
sub-007C: True group = HC
sub-008P: True group = MDD
sub-010P: True group = MDD
sub-013C: True group = HC
sub-014C: True group = HC
sub-014P: True group = MDD
sub-016C: True group = HC
sub-017C: True group = HC
sub-018C: True group = HC
sub-020P: True group = MDD
sub-021C: True group = HC
sub-024C: True group = HC
sub-027C: True group = HC
sub-029C: True group = HC
sub-030C: True group = HC
sub-031C: True group = HC
sub-033P: True group = MDD
sub-037P: True group = MDD
sub-046P: True group = MDD
sub-066P: True group = MDD
sub-067P: True group = MDD

Incorrectly classified subjects:
sub-003P: True group = MDD, Predicted as = HC
sub-005P: True group = MDD, Predicted as = HC
sub-007P: True group = MDD, Predicted as = HC
sub-009C: True group = HC, Predicted as = MDD
sub-015C: True group = HC, Predicted as = MDD
sub-019C: True group = HC, Predicted as = MDD
sub-020C: True group = HC, Predicted as = MDD
sub-025C: True group = HC, Predicted as = MDD
sub-026C: True group = HC, Predicted as = MDD
sub-028C: True group = HC, Predicted as = MDD
sub-031P: True group = MDD, Predicted as = HC
sub-032P: True group = MDD, Predicted as = HC
sub-042P: True group = MDD, Predicted as = HC
sub-048P: True group = MDD, Predicted as = HC
sub-052P: True group = MDD, Predicted as = HC
sub-075P: True group = MDD, Predicted as = HC

Feature Importance with best parameters:
auditory: 0.539537
visual: 0.494309
motor: 0.241168
```

### Features: Transmodal regions (salience, fpn, dmn, limbic)
```
Best parameters: {'C': 0.5, 'gamma': 'scale', 'kernel': 'linear'}
Best cross-validation accuracy: 0.7894736842105263

Features used in classification:
- salience
- fpn
- dmn
- limbic

LOOCV Accuracy with best parameters: 0.789
95% Confidence Interval: [0.660, 0.919]

Correct predictions: 30 out of 38

Correctly classified subjects:
sub-005P: True group = MDD
sub-007C: True group = HC
sub-008P: True group = MDD
sub-009C: True group = HC
sub-010P: True group = MDD
sub-013C: True group = HC
sub-014C: True group = HC
sub-014P: True group = MDD
sub-015C: True group = HC
sub-016C: True group = HC
sub-018C: True group = HC
sub-020P: True group = MDD
sub-021C: True group = HC
sub-024C: True group = HC
sub-025C: True group = HC
sub-026C: True group = HC
sub-027C: True group = HC
sub-028C: True group = HC
sub-029C: True group = HC
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
sub-003P: True group = MDD, Predicted as = HC
sub-006C: True group = HC, Predicted as = MDD **Note that this subject was correctly classified in the unimodal regions classification**
sub-007P: True group = MDD, Predicted as = HC
sub-017C: True group = HC, Predicted as = MDD **Note that this subject was correctly classified in the unimodal regions classification**
sub-019C: True group = HC, Predicted as = MDD
sub-020C: True group = HC, Predicted as = MDD
sub-031P: True group = MDD, Predicted as = HC
sub-048P: True group = MDD, Predicted as = HC

Feature Importance with best parameters:
salience: 0.839216
fpn: 0.794969
dmn: 0.281842
limbic: 0.254405
```
## Classifications with inidivual transmodal regions
The goal of this next round of classifications is to see if any single transmodal region can be used to classify the subjects with greater or equal accuracy.

### Features: DMN
```
Best parameters: {'C': 1.0, 'gamma': 'scale', 'kernel': 'rbf'}
Best cross-validation accuracy: 0.7631578947368421

Features used in classification:
- dmn

LOOCV Accuracy with best parameters: 0.763
95% Confidence Interval: [0.628, 0.898]

Correct predictions: 29 out of 38

Correctly classified subjects:
sub-007C: True group = HC
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
sub-020C: True group = HC
sub-021C: True group = HC
sub-024C: True group = HC
sub-025C: True group = HC
sub-026C: True group = HC
sub-027C: True group = HC
sub-028C: True group = HC
sub-029C: True group = HC
sub-030C: True group = HC
sub-031C: True group = HC
sub-033P: True group = MDD
sub-037P: True group = MDD
sub-042P: True group = MDD
sub-046P: True group = MDD
sub-052P: True group = MDD
sub-066P: True group = MDD
sub-067P: True group = MDD

Incorrectly classified subjects:
sub-003P: True group = MDD, Predicted as = HC
sub-005P: True group = MDD, Predicted as = HC **This subject was correctly classified in the transmodal regions classification**
sub-006C: True group = HC, Predicted as = MDD
sub-007P: True group = MDD, Predicted as = HC
sub-020P: True group = MDD, Predicted as = HC **This subject was correctly classified in the unimodal and transmodal regions classifications**
sub-031P: True group = MDD, Predicted as = HC
sub-032P: True group = MDD, Predicted as = HC **This subject was correctly classified in the transmodal regions classification**
sub-048P: True group = MDD, Predicted as = HC
sub-075P: True group = MDD, Predicted as = HC **This subject was correctly classified in the transmodal regions classification**
```

### Features: Salience
```
Best parameters: {'C': 0.5, 'gamma': 'scale', 'kernel': 'linear'}
Best cross-validation accuracy: 0.7631578947368421

Features used in classification:
- salience

LOOCV Accuracy with best parameters: 0.763
95% Confidence Interval: [0.628, 0.898]

Correct predictions: 29 out of 38

Correctly classified subjects:
sub-005P: True group = MDD
sub-006C: True group = HC
sub-007C: True group = HC
sub-008P: True group = MDD
sub-010P: True group = MDD
sub-014C: True group = HC
sub-014P: True group = MDD
sub-015C: True group = HC
sub-016C: True group = HC
sub-018C: True group = HC
sub-020P: True group = MDD
sub-021C: True group = HC
sub-024C: True group = HC
sub-025C: True group = HC
sub-026C: True group = HC
sub-027C: True group = HC
sub-029C: True group = HC
sub-030C: True group = HC
sub-031C: True group = HC
sub-031P: True group = MDD
sub-032P: True group = MDD
sub-033P: True group = MDD
sub-037P: True group = MDD
sub-046P: True group = MDD
sub-048P: True group = MDD
sub-052P: True group = MDD
sub-066P: True group = MDD
sub-067P: True group = MDD
sub-075P: True group = MDD

Incorrectly classified subjects:
sub-003P: True group = MDD, Predicted as = HC
sub-007P: True group = MDD, Predicted as = HC
sub-009C: True group = HC, Predicted as = MDD
sub-013C: True group = HC, Predicted as = MDD
sub-017C: True group = HC, Predicted as = MDD
sub-019C: True group = HC, Predicted as = MDD
sub-020C: True group = HC, Predicted as = MDD
sub-028C: True group = HC, Predicted as = MDD
sub-042P: True group = MDD, Predicted as = HC

Feature Importance with best parameters:
salience: 1.619685
```

### Features: FPN
```
Best parameters: {'C': 2.0, 'gamma': 'scale', 'kernel': 'linear'}
Best cross-validation accuracy: 0.8421052631578947

Features used in classification:
- fpn

LOOCV Accuracy with best parameters: 0.842
95% Confidence Interval: [0.726, 0.958]

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
sub-006C: True group = HC, Predicted as = MDD **This subject was correctly classified in the unimodal regions classification**
sub-007C: True group = HC, Predicted as = MDD **This subject was correctly classified in the unimodal, transmodal and dmn regions classifications**
sub-020C: True group = HC, Predicted as = MDD **This subject was correctly classified in the dmn regions classifications**
sub-029C: True group = HC, Predicted as = MDD **This subject was correctly classified in the unimodal, transmodal and dmn regions classification**
sub-031P: True group = MDD, Predicted as = HC
sub-048P: True group = MDD, Predicted as = HC

Feature Importance with best parameters:
fpn: 1.660805
```