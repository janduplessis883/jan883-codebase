import warnings
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
import xgboost as xgb
from sklearn.linear_model import LogisticRegression
from sklearn.inspection import permutation_importance
from sklearn.model_selection import cross_validate, learning_curve, StratifiedKFold
from sklearn.metrics import (
    make_scorer,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    auc,
    RocCurveDisplay,
)
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
)
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from yellowbrick.regressor import ResidualsPlot, PredictionError
from yellowbrick.classifier import DiscriminationThreshold, PrecisionRecallCurve
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler
import joblib
from datetime import datetime
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import (
    RandomForestRegressor,
    GradientBoostingRegressor,
    AdaBoostRegressor,
)
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    AdaBoostClassifier,
)
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from tqdm import tqdm
from IPython.display import HTML, Markdown, display

warnings.filterwarnings("ignore")


def ml0():
    message = """<b>Model Selection — Choosing the right Model.</b> <BR>
- Feature Importance Plot<BR>
- Evaluate Classification Model<BR>
- Evaluate Regression Model<BR>
- Test Regression Models<BR>
- Test Classification Modeks<BR>
<b>Custom Functions</b><br>
- <code>feature_importance_plot(model, X, y)</code> Plot Feature Importance using a single model.<BR>
- <code>evaluate_classification_model(model, X, y, cv=5)</code> Plot peformance metrics of single classification model.<BR>
- <code>evaluate_regression_model(model, X, y)</code> Plot peformance metrics of single regression model.<BR>
- <code>test_regression_models(X, y, test_size=0.2, random_state=None, scale_data=False)</code> Test Regression models.<BR>
- <code>test_classification_models(X, y, test_size=0.2, random_state=None, scale_data=False)</code> Test Classification models.<BR>
"""
    html_message = f"""
        <span style="color: #345a69; font-size: 12px;">{message}</span>
    """
    display(HTML(html_message))


def feature_importance_comparison(X_train, y_train):
    def feature_importance_sorted(
        classification_model_input, X_train, y_train, feature_importance_input=None
    ):
        if classification_model_input is not None:
            some_model = classification_model_input
            some_model.fit(X_train, y_train)
            feature_importances = some_model.feature_importances_
        else:
            feature_importances = feature_importance_input
        feature_importances_sorted = sorted(
            zip(X_train.columns, feature_importances), key=lambda x: x[1], reverse=True
        )
        df_feature_importances = pd.DataFrame(
            feature_importances_sorted, columns=["Feature", "Importance"]
        )
        df_feature_importances["rank"] = range(1, len(df_feature_importances) + 1)
        return df_feature_importances

    # Decision Tree Classifier Feature Importance
    dtc_fi = feature_importance_sorted(DecisionTreeClassifier(), X_train, y_train)
    dtc_fi = dtc_fi.rename(columns={"Importance": "imp_dtc", "rank": "rank_dtc"})

    # Random Forest Classifier Feature Importance
    rfc_fi = feature_importance_sorted(
        RandomForestClassifier(), X_train, y_train.values.ravel()
    )
    rfc_fi = rfc_fi.rename(columns={"Importance": "imp_rfc", "rank": "rank_rfc"})

    # XGB Classifier Feature Importance
    xgb_fi = feature_importance_sorted(xgb.XGBClassifier(), X_train, y_train)
    xgb_fi = xgb_fi.rename(columns={"Importance": "imp_xgb", "rank": "rank_xgb"})

    # Logistic Regression Feature Importance
    lr = LogisticRegression(max_iter=10000)
    lr.fit(X_train, y_train.values.ravel())
    feature_importances = lr.coef_[0]  # Assuming binary classification
    lr_fi = feature_importance_sorted(
        None, X_train, y_train.values.ravel(), feature_importances
    )
    lr_fi = lr_fi.rename(columns={"Importance": "imp_lr", "rank": "rank_lr"})

    # Merge the results from all models
    merged_df = (
        dtc_fi.merge(rfc_fi, on="Feature", how="left")
        .merge(xgb_fi, on="Feature", how="left")
        .merge(lr_fi, on="Feature", how="left")
    )

    return merged_df


def evaluate_classification_model(model, X, y, cv=5):
    """
    Evaluates the performance of a model using cross-validation, a learning curve, and a ROC curve.

    Parameters:
    - model: estimator instance. The model to evaluate.
    - X: DataFrame. The feature matrix.
    - y: Series. The target vector.
    - cv: int, default=5. The number of cross-validation folds.

    Returns:
    - None
    """
    print(model)
    # Cross validation
    scoring = {
        "accuracy": make_scorer(accuracy_score),
        "precision": make_scorer(precision_score, average="macro"),
        "recall": make_scorer(recall_score, average="macro"),
        "f1_score": make_scorer(f1_score, average="macro"),
    }

    scores = cross_validate(model, X, y, cv=cv, scoring=scoring, n_jobs=-1)

    # Compute means and standard deviations for each metric, and collect in a dictionary
    mean_std_scores = {
        metric: (np.mean(score_array), np.std(score_array))
        for metric, score_array in scores.items()
    }

    # Create a DataFrame from the mean and std dictionary and display as HTML
    scores_df = pd.DataFrame(mean_std_scores, index=["Mean", "Standard Deviation"]).T
    display(HTML(scores_df.to_html()))

    # Learning curve
    train_sizes = np.linspace(0.1, 1.0, 5)
    train_sizes, train_scores, test_scores = learning_curve(
        model, X, y, cv=cv, train_sizes=train_sizes
    )
    train_scores_mean = np.mean(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)

    # Define the figure and subplots
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    axs[0].plot(
        train_sizes, train_scores_mean, "o-", color="#a10606", label="Training score"
    )
    axs[0].plot(
        train_sizes,
        test_scores_mean,
        "o-",
        color="#6b8550",
        label="Cross-validation score",
    )
    axs[0].set_xlabel("Training examples")
    axs[0].set_ylabel("Score")
    axs[0].legend(loc="best")
    axs[0].set_title("Learning curve")

    # ROC curve
    cv = StratifiedKFold(n_splits=cv)
    tprs = []
    aucs = []
    mean_fpr = np.linspace(0, 1, 100)

    for i, (train, test) in enumerate(cv.split(X, y)):
        model.fit(X.iloc[train], y.iloc[train])
        viz = RocCurveDisplay.from_estimator(
            model,
            X.iloc[test],
            y.iloc[test],
        )
        interp_tpr = np.interp(mean_fpr, viz.fpr, viz.tpr)
        interp_tpr[0] = 0.0
        tprs.append(interp_tpr)
        aucs.append(viz.roc_auc)

    mean_tpr = np.mean(tprs, axis=0)
    mean_tpr[-1] = 1.0
    mean_auc = auc(mean_fpr, mean_tpr)
    std_auc = np.std(aucs)

    axs[1].plot(
        mean_fpr,
        mean_tpr,
        color="#023e8a",
        label=r"Mean ROC (AUC = %0.2f $\pm$ %0.2f)" % (mean_auc, std_auc),
        lw=2,
        alpha=0.6,
    )

    std_tpr = np.std(tprs, axis=0)
    tprs_upper = np.minimum(mean_tpr + std_tpr, 1)
    tprs_lower = np.maximum(mean_tpr - std_tpr, 0)
    axs[1].fill_between(
        mean_fpr,
        tprs_lower,
        tprs_upper,
        color="#023e8a",
        alpha=0.2,
        label=r"$\pm$ 1 std. dev.",
    )

    axs[1].plot(
        [0, 1], [0, 1], linestyle="--", lw=2, color="#a10606", label="Chance", alpha=0.6
    )
    axs[1].legend(loc="lower right")
    axs[1].set_title("Mean ROC curve with Cross-Validation")

    # Show plots
    plt.tight_layout()
    plt.show()


# Permutation feature importance
def feature_importance_plot(model, X, y):
    """
    Displays the feature importances of a model using permutation importance.

    Parameters:
    - model: estimator instance. The model to evaluate.
    - X: DataFrame. The feature matrix.
    - y: Series. The target vector.

    Returns:
    - Permutation importance plot
    """
    # Train the model
    model.fit(X, y)

    # Calculate permutation importance
    result = permutation_importance(model, X, y, n_repeats=10)
    sorted_idx = result.importances_mean.argsort()

    # Permutation importance plot
    plt.figure(figsize=(10, 5))
    plt.boxplot(
        result.importances[sorted_idx].T, vert=False, labels=X.columns[sorted_idx]
    )
    plt.title("Permutation Importances")
    plt.show()


import pandas as pd
from scipy.stats import ttest_ind


def evaluate_regression_model(model, X, y):
    # Split the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Fit the model on the training data
    model.fit(X_train, y_train)

    # Predict on test data
    y_pred = model.predict(X_test)

    # Metrics
    print("Mean Absolute Error (MAE):", mean_absolute_error(y_test, y_pred))
    print("Mean Squared Error (MSE):", mean_squared_error(y_test, y_pred))
    print(
        "Root Mean Squared Error (RMSE):",
        np.sqrt(mean_squared_error(y_test, y_pred)),
    )
    print("R-squared (R2):", r2_score(y_test, y_pred))

    # Create figure
    fig, axs = plt.subplots(2, 2, figsize=(16, 12))

    # Learning curve
    train_sizes, train_scores, test_scores = learning_curve(model, X, y, cv=5)
    train_scores_mean = np.mean(train_scores, axis=1)
    test_scores_mean = np.mean(test_scores, axis=1)
    axs[0, 0].plot(
        train_sizes,
        train_scores_mean,
        "o-",
        color="#a10606",
        label="Training score",
    )
    axs[0, 0].plot(
        train_sizes,
        test_scores_mean,
        "o-",
        color="#6b8550",
        label="Cross-validation score",
    )
    axs[0, 0].set_title("Learning Curve")
    axs[0, 0].set_xlabel("Training Examples")
    axs[0, 0].set_ylabel("Score")
    axs[0, 0].legend(loc="best")
    axs[0, 1].axis("off")  # Turn off unused subplot

    # Residuals plot
    visualizer = ResidualsPlot(model, ax=axs[1, 0])
    visualizer.fit(X_train, y_train)
    visualizer.score(X_test, y_test)
    visualizer.finalize()

    # Prediction error plot
    visualizer = PredictionError(model, ax=axs[1, 1])
    visualizer.fit(X_train, y_train)
    visualizer.score(X_test, y_test)
    visualizer.finalize()

    # Show all plots
    plt.tight_layout()
    plt.show()


def test_regression_models(X, y, test_size=0.2, random_state=None, scale_data=False):
    """
    Tests multiple regression models from sklearn on the given dataset.

    Parameters:
    - X: DataFrame or array-like. The feature set.
    - y: Series or array-like. The target variable.
    - test_size: float, default=0.2. The proportion of the dataset to include in the test split.
    - random_state: int, default=None. Random state for reproducibility.
    - scale_data: bool, default=False. Whether to scale the data using StandardScaler.

    Returns:
    - results_df: DataFrame. A DataFrame containing the model name, R² score, MSE, RMSE, and MAE for each model.
    """

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    # Define a list of regression models to test
    models = {
        "Linear Regression": LinearRegression(),
        "Ridge Regression": Ridge(),
        "Lasso Regression": Lasso(),
        "ElasticNet Regression": ElasticNet(),
        "Decision Tree": DecisionTreeRegressor(),
        "Random Forest": RandomForestRegressor(),
        "Gradient Boosting": GradientBoostingRegressor(),
        "AdaBoost": AdaBoostRegressor(),
        "Support Vector Regressor": SVR(),
        "K-Nearest Neighbors": KNeighborsRegressor(),
        "MLP Regressor": MLPRegressor(max_iter=1000),
        "Gaussian Process": GaussianProcessRegressor(),
    }

    # DataFrame to store results
    results = []

    # Loop over models and evaluate each one with a progress bar
    for name, model in tqdm(models.items(), desc="Testing Models"):
        # Create a pipeline if scaling is requested
        if scale_data:
            pipeline = Pipeline([("scaler", StandardScaler()), ("regressor", model)])
            pipeline.fit(X_train, y_train)
            y_pred = pipeline.predict(X_test)
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

        # Calculate metrics
        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = np.sqrt(mse)
        mae = mean_absolute_error(y_test, y_pred)

        # Append the results to the list
        results.append(
            {"Model": name, "R² Score": r2, "MSE": mse, "RMSE": rmse, "MAE": mae}
        )

    # Convert the results list to a DataFrame
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(by="R² Score", ascending=False).reset_index(
        drop=True
    )

    return results_df


def test_classification_models(
    X, y, test_size=0.2, random_state=None, scale_data=False
):
    """
    Tests multiple classification models from sklearn on the given dataset.

    Parameters:
    - X: DataFrame or array-like. The feature set.
    - y: Series or array-like. The target variable.
    - test_size: float, default=0.2. The proportion of the dataset to include in the test split.
    - random_state: int, default=None. Random state for reproducibility.
    - scale_data: bool, default=False. Whether to scale the data using StandardScaler.

    Returns:
    - results_df: DataFrame. A DataFrame containing the model name, accuracy, precision, recall, F1 score, and ROC-AUC score for each model.
    """

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    # Define a list of classification models to test
    models = {
        "Logistic Regression": LogisticRegression(),
        "Decision Tree": DecisionTreeClassifier(),
        "Random Forest": RandomForestClassifier(),
        "Gradient Boosting": GradientBoostingClassifier(),
        "AdaBoost": AdaBoostClassifier(),
        "Support Vector Classifier": SVC(probability=True),
        "K-Nearest Neighbors": KNeighborsClassifier(),
        "MLP Classifier": MLPClassifier(max_iter=1000),
        "Naive Bayes": GaussianNB(),
    }

    # DataFrame to store results
    results = []

    # Loop over models and evaluate each one with a progress bar
    for name, model in tqdm(models.items(), desc="Testing Models"):
        # Create a pipeline if scaling is requested
        if scale_data:
            pipeline = Pipeline([("scaler", StandardScaler()), ("classifier", model)])
            pipeline.fit(X_train, y_train)
            y_pred = pipeline.predict(X_test)
            y_proba = (
                pipeline.predict_proba(X_test)[:, 1]
                if hasattr(pipeline, "predict_proba")
                else None
            )
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_proba = (
                model.predict_proba(X_test)[:, 1]
                if hasattr(model, "predict_proba")
                else None
            )

        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average="binary")
        recall = recall_score(y_test, y_pred, average="binary")
        f1 = f1_score(y_test, y_pred, average="binary")
        roc_auc = roc_auc_score(y_test, y_proba) if y_proba is not None else None

        # Append the results to the list
        results.append(
            {
                "Model": name,
                "Accuracy": accuracy,
                "Precision": precision,
                "Recall": recall,
                "F1 Score": f1,
                "ROC-AUC": roc_auc,
            }
        )

    # Convert the results list to a DataFrame
    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values(by="Accuracy", ascending=False).reset_index(
        drop=True
    )

    return results_df
