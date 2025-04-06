## Group Project
# Logistic Regression R Code

#Libraries
library(tidyverse)  # For data manipulation
library(summarytools)  # For quick dataset summary
library(caret)  # For checking class balance
library(naniar) # For missing value visualization
library(data.table)
library(rpart)
library(rpart.plot)
library(glm2)
library(caTools)
library(ggplot2)
library(dplyr)
library(car)
library(quantreg)
library(neuralnet)

#wd
setwd("Analytics II Advanced Predictive Techniques/BC2407 Course Materials/Group project")

data <- fread("hotel_cleaned.csv", stringsAsFactors = T)

#Logistic reg
set.seed(2025)

# Logistic regression model
model <- glm(is_canceled ~ ., data = data, family = binomial())

# Summary of the model
summary(model)

# 70-30 train-test split (SMOTE)
trainset <- fread("train.csv", stringsAsFactors = T)
testset <- fread("test.csv", stringsAsFactors = T)

m1 <- glm(is_canceled ~ ., data = trainset, family = binomial())
summary(m1)
vif(m1)

# Convert trainset$is_canceled to numeric (1/0)
trainset$is_canceled_numeric <- ifelse(trainset$is_canceled == TRUE, 1, 0)
# Convert testset$is_canceled to numeric (1/0)
testset$is_canceled_numeric <- ifelse(testset$is_canceled == TRUE, 1, 0)

#Classify in the trainset data
pred.train.m <- predict(m1, type = 'response') #response = probabilities
pred.trainclass <- ifelse(pred.train.m > 0.5, "1", "0")

#Create confusion matrix for train set data
table(actual = trainset$is_canceled, predictions = pred.trainclass)
mean(trainset$is_canceled == pred.trainclass)

#Classify in the testset data
testset$assigned_room_type_L <- as.logical(testset$assigned_room_type_L) # due to error
pred.test.m <- predict(m1, type = 'response', newdata = testset) #response = probabilities
pred.testclass <- ifelse(pred.test.m > 0.5, "1", "0")

#Create confusion matrix for test set data
table(actual = testset$is_canceled, prediction = pred.testclass)
mean(testset$is_canceled == pred.testclass)

# Calculate mean accuracy
mean(trainset$is_canceled_numeric == pred.trainclass) #trainset
mean(testset$is_canceled_numeric == pred.testclass) #testset

# Confusion matrix for test set data
cm_test <- table(actual = testset$is_canceled, prediction = pred.testclass)
print(cm_test)

# Class 1 (Cancelled) metrics for testset
TP_test_class1 <- cm_test["1", "1"]  # True Positives for class 1
FP_test_class1 <- cm_test["0", "1"]  # False Positives for class 1
TN_test_class1 <- cm_test["0", "0"]  # True Negatives for class 1
FN_test_class1 <- cm_test["1", "0"]  # False Negatives for class 1

precision_test_class1 <- TP_test_class1 / (TP_test_class1 + FP_test_class1)
recall_test_class1 <- TP_test_class1 / (TP_test_class1 + FN_test_class1)
f1_score_test_class1 <- 2 * (precision_test_class1 * recall_test_class1) / (precision_test_class1 + recall_test_class1)

# Class 0 (Not Cancelled) metrics for testset
TP_test_class0 <- cm_test["0", "0"]  # True Positives for class 0
FP_test_class0 <- cm_test["1", "0"]  # False Positives for class 0
TN_test_class0 <- cm_test["1", "1"]  # True Negatives for class 0
FN_test_class0 <- cm_test["0", "1"]  # False Negatives for class 0

precision_test_class0 <- TP_test_class0 / (TP_test_class0 + FP_test_class0)
recall_test_class0 <- TP_test_class0 / (TP_test_class0 + FN_test_class0)
f1_score_test_class0 <- 2 * (precision_test_class0 * recall_test_class0) / (precision_test_class0 + recall_test_class0)

# Combine all metrics for test set into a single output
test_metrics <- data.frame(
  Class = c("Class 1", "Class 0"),
  Precision = c(precision_test_class1, precision_test_class0),
  Recall = c(recall_test_class1, recall_test_class0),
  F1_Score = c(f1_score_test_class1, f1_score_test_class0)
)

# Print the combined output for test set metrics
print(test_metrics)