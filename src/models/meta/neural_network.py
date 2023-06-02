# General
import numpy as np
import pandas as pd

# Modelling
from tensorflow import keras

from keras.layers import Dense
from sklearn.utils import compute_class_weight
from sklearn.model_selection import KFold

# Project
from src.structure import Config
import pipelines


root_path = Config.root_dir()
data_destination = '/notebooks/model_comparison_cache_2/'


def write_training_accuracy(file_name: str, fold_histories: dict):
    df = pd.DataFrame(fold_histories)
    df.to_csv(root_path + data_destination + file_name, index=False)


def neural_network_process(df: pd.DataFrame, taxon_target: str, k_cluster, model_name: str, score_file: str, validation_file:str):
    X, y, lb, classes = pipelines.neural_network_data(df, taxon_target, k_cluster, validation_file)
    folds = 4
    kf = KFold(n_splits=folds)
    mean_accuracy, mean_loss = train_neural_network(X, y, kf, classes, model_name, score_file)
    return mean_accuracy, mean_loss


def train_neural_network(X, y, kf, classes: int, model_name: str, score_file: str):
    input_dimension = len(X.columns)

    fold_histories = []
    eval_accuracy = []
    eval_loss = []
    epoch_num = 10
    fold_ind = 0


    for train_index, test_index in kf.split(X, y):
        # Generate test and validation training sets
        X_train = X.iloc[train_index]
        y_train = y[train_index]

        X_val = X.iloc[test_index]
        y_val = y[test_index]

        # Create a new model
        model = make_model(input_dimension, classes)

        model.compile(optimizer='adam',
                      loss='categorical_crossentropy',
                      metrics=[keras.metrics.CategoricalAccuracy()])

        # Weight the training by presence of each class.
        y_cat = np.argmax(y_train, axis=1)
        unique_classes = np.unique(y_cat)
        weight_values = compute_class_weight(class_weight='balanced', classes=unique_classes, y=y_cat)
        weights = dict(zip(unique_classes, weight_values))

        # Training History
        history = model.fit(X_train.to_numpy(), y_train, epochs=epoch_num, class_weight=weights, verbose=0)

        hist_df = pd.DataFrame(history.history)
        fold_histories.append(hist_df['categorical_accuracy'].values.tolist())

        # Validation
        results = model.evaluate(X_val, y_val, verbose=0)
        eval_accuracy = results[1]
        eval_loss = results[0]

        ## Display while training
        training_mean_accuracy = np.mean(fold_histories[fold_ind])
        print(f'training set accuracy: {training_mean_accuracy}')
        print(f'Validation set accuracy: {results[1]}')

        fold_ind = fold_ind + 1

    model.save(root_path + data_destination + model_name)
    write_training_accuracy(score_file, fold_histories)
    return np.mean(eval_accuracy), np.mean(eval_loss)


def make_model(input_dimension: int, classes: int) -> keras.Sequential:
    model = keras.Sequential()
    model.add(Dense(input_dimension, input_shape=(input_dimension,), activation='relu'))
    model.add(Dense(80, activation='relu'))
    model.add(Dense(60, activation='relu'))
    model.add(Dense(classes, activation='softmax'))
    return model