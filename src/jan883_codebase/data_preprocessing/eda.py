import warnings
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import HTML, Markdown, display

from scipy.stats import ttest_ind
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
import joblib
from datetime import datetime

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

# from imblearn.over_sampling import SMOTE

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
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer
from sklearn.cluster import KMeans
from yellowbrick.cluster import InterclusterDistance
from sklearn.cluster import KMeans
from yellowbrick.cluster import SilhouetteVisualizer
from yellowbrick.model_selection import learning_curve
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.model_selection import StratifiedKFold, KFold
from yellowbrick.model_selection import rfecv
from sklearn.impute import SimpleImputer
import pickle
from scipy.stats import pearsonr


warnings.filterwarnings("ignore")


def eda0():
    message = "<b>EDA Level 0 - Pure Understanding of Original Data</b> <BR>Basic check on the column datatype, null counts, distinct values, to get a better understanding of the data. I also created a distinct values count dictionary where I go the top 10 counts and their distinct values displayed so I could roughly gauge how significant the distinct values are in the dataset.<BR><b>Custom Functions</b><br> - <code>inspect_df(df)</code> Run df.head(), df.describe(), df.isna().sum() & df.duplicated().sum() on your dataframe. <br> - <code>column_summary(df)</code> Create a dataframe with column info, dtype, value_counts, etc.<br> - <code>column_summary_plus(df)</code> Create a dataframe with column info, dtype, value_counts, plus df.decsribe() info.<br> - <code>univariate_analysis(df)</code> Perform Univariate Analysis of numeric columns."
    html_message = f"""
        <span style="color: #274562; font-size: 12px;">{message}</span>
    """
    display(HTML(html_message))


def eda1():
    message = """<b>EDA Level 1 — Transformation of Original Data</b> <BR>I standardized the column names by converting them to lowercase and replacing spaces with underscores, ensuring they are more generic and categorized for easier interpretation. Missing values in the dataset were filled with sensible values to address null or NaN entries. I updated the data types of columns to ensure they are more appropriate for the data they represent. To ensure the data’s accuracy, I conducted validation checks. Categorical features were mapped or binned into meaningful groups for better analysis, and I applied Label Encoding to one column while using One-Hot Encoding for another. Additionally, missing values were imputed as part of the preprocessing steps.
<b>Custom Functions</b><br>- <code>update_column_names(df)</code> Update Column names, replace " " with "_".<BR>
- <code>label_encode_column(df, col_name)</code> Label encode a df column returing a df with the new column (original col dropped).<BR>
- <code>one_hot_encode_column(df, col_name)</code> One Hot Encode a df column returing a df with the new column (original col dropped).<BR>
- <code>train_no_outliers = remove_outliers_zscore(train, threshold=3)</code> Remove outliers using Z score.<BR>
- <code>df_imputed = impute_missing_values(df, strategy='median')</code> Impute missing values in DF
"""

    html_message = f"""
        <span style="color: #274562; font-size: 12px;">{message}</span>
    """
    display(HTML(html_message))


def eda2():
    message = """<b>EDA Level 2 — Understanding of Transformed Data</b> <BR>
I conducted a correlation analysis to understand relationships between variables and calculated Information Value (IV) and Weight of Evidence (WOE) values to assess the predictive power of features, aiming for an IV range of 0.1 to 0.5 (with values below 0.1 being weak and above 0.5 potentially too strong). Feature importance was evaluated using models, complemented by statistical tests for deeper insights. I also created QQ plots to assess data normality and performed further analysis on the imputed data. For scaling, the scale_df(X) method was used during exploration since it does not scale X_test. For a complete scaling solution, scale_X_train_X_test(X_train, X_test, scaler="standard", save_scaler=False) was applied, which scales both training and test sets, fits and transforms the data, and optionally saves the scaler to disk.
<b>Custom Functions</b><br>- <code>correlation_analysis(df, width=16, height=12)</code> Correlation Heatmap & Maximum pairwise correlation.<BR>
- <code>check_multicollinearity(df)</code> Check for Multicollinearity.<BR>
- <code>newDF, woeDF = iv_woe(df, target, bins=10, show_woe=False)</code> Returns newDF, woeDF. IV / WOE Values - Information Value (IV) quantifies the prediction power of a feature. We are looking for IV of 0.1 to 0.5. For those with IV of 0, there is a high chance it is the way it is due to imbalance of data, resulting in lack of binning. Keep this in mind during further analysis.<BR>
- <code>individual_t_test_classification(df, y_column, y_value_1, y_value_2, list_of_features, alpha_val=0.05, sample_frac=1.0, random_state=None)</code> Statistical test of individual features - Classification problem.<BR>
- <code>individual_t_test_regression(df, y_column, list_of_features, alpha_val=0.05, sample_frac=1.0, random_state=None)</code> Statistical test of individual features - Regressions problem.<BR>
- <code>create_qq_plots(df, reference_col)</code> Create QQ plots of the features in a dataframe.<BR>
- <code>volcano_plot(df, reference_col)</code> Create Volcano Plot with P-values.<BR>
- <code>X, y = define_X_y(df, target)</code> Define X and y..<BR>
- <code>X_train, X_test, y_train, y_test = train_test_split_custom(X, y, test_size=0.2, random_state=42)</code> Split train, test.<BR>
- <code>X_train, X_val, X_test, y_train, y_val, y_test = train_val_test_split(X, y, val_size=0.2, test_size=0.2, random_state=42)</code> Split train, val, test.<BR>
- <code>X_train_res, y_train_res = oversample_SMOTE(X_train, y_train, sampling_strategy="auto", k_neighbors=5, random_state=42)</code> Oversample minority class.<BR>
- <code>scaled_X = scale_df(X, scaler='standard')</code> only scales X, does not scale X_test or X_val. <BR>
- <code>scaled_X_train, scaled_X_test = scale_X_train_X_test(X_train, X_test, scaler="standard", save_scaler=False)</code> Standard, MinMax and Robust Scaler. X_train uses fit_transform, X_test uses transform.<BR>
- <code>sample_df(df, n_samples)</code> Take a sample of the full df.<BR>
"""

    html_message = f"""
        <span style="color: #274562; font-size: 12px;">{message}</span>
    """
    display(HTML(html_message))


def model():
    message = """<b>Model Selection — Choosing the right Model.</b> <BR>
 generated a feature importance plot to visualize the significance of features and created learning curves for both regression and classification tasks to assess model performance over varying dataset sizes. Recursive Feature Elimination with Cross-Validation (RFECV) was plotted for both regression and classification to identify the optimal subset of features. Classification and regression models were thoroughly evaluated, including assessing multiple models to determine the best-performing ones based on relevant metrics. Additionally, clustering analysis was conducted using the Elbow Method, Intercluster Distance, and Silhouette Visualizer to evaluate cluster quality and identify optimal cluster numbers.
<b>Custom Functions</b><br>
- <code>feature_importance_plot(model, X, y)</code> Plot Feature Importance using a single model.<BR>
- <code>plot_learning_curve(X, y, problem_type='classification', scoring='accuracy')</code> Plot Learning Curve using a single model, classification or regression. <BR>
- <code>plot_rfecv(X, y, problem_type='classification', cv_splits=5, scoring='f1_weighted')</code> Recursive Feature Elimination using a single model - RandomForestClassifer/Regressor.<BR>
- <code>evaluate_classification_model(model, X, y, cv=5)</code> Plot peformance metrics of single classification model.<BR>
- <code>evaluate_regression_model(model, X, y)</code> Plot peformance metrics of single regression model.<BR>
- <code>best_regression_models(X, y, test_size=0.2, random_state=None, scale_data=False)</code> Test Regression models.<BR>
- <code>best_classification_models(X, y, test_size=0.2, random_state=None, scale_data=False)</code> Test Classification models.<BR>
- <code>plot_elbow_method(scaled_df, k_range=(4, 12), random_state=None)</code> Plot Elbow Method to find optimal number of clusters.<BR>
- <code>plot_intercluster_distance(X, n_clusters=6, random_state=None)</code> Plot Intercluster Distance to find optimal number of clusters.<BR>
- <code>plot_silhouette_visualizer(X, n_clusters=4, random_state=42)</code> Plot Silhouette Visualizer to find optimal number of clusters.<br>

"""
    html_message = f"""
        <span style="color: #274562; font-size: 12px;">{message}</span>
    """
    display(HTML(html_message))


def convert_to_datetime(df, columns, day_first):
    """
    Converts the specified columns in the DataFrame to datetime format.

    Args:
        df (pd.DataFrame): The input DataFrame.
        columns (list): A list of column names to be converted.
        day_first (bool): Whether to use day first or month

    Returns:
        pd.DataFrame: The modified DataFrame with the specified columns as datetime.
    """
    for col in columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=day_first)
        else:
            raise ValueError(f"Column '{col}' not found in DataFrame.")
    display(df.info())
    return df


def column_summary(df):
    """
    Calculate summary statistics for each column in a Pandas DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame

    Returns:
        pd.DataFrame: Result DataFrame with summary statistics for each column
    """
    summary_data = []

    for col_name in df.columns:
        col_dtype = df[col_name].dtype
        num_of_nulls = df[col_name].isnull().sum()
        num_of_non_nulls = df[col_name].notnull().sum()
        num_of_distinct_values = df[col_name].nunique()

        if num_of_distinct_values <= 10:
            distinct_values_counts = df[col_name].value_counts().to_dict()
        else:
            top_10_values_counts = df[col_name].value_counts().head(10).to_dict()
            distinct_values_counts = {
                k: v
                for k, v in sorted(
                    top_10_values_counts.items(), key=lambda item: item[1], reverse=True
                )
            }

        summary_data.append(
            {
                "col_name": col_name,
                "col_dtype": col_dtype,
                "num_of_nulls": num_of_nulls,
                "num_of_non_nulls": num_of_non_nulls,
                "num_of_distinct_values": num_of_distinct_values,
                "distinct_values_counts": distinct_values_counts,
            }
        )

    summary_df = pd.DataFrame(summary_data)
    return summary_df


def column_summary_plus(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate summary statistics for each column in a Pandas DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame

    Returns:
        pd.DataFrame: Result DataFrame with summary statistics for each column
    """

    result = []

    for col_name, col in df.items():
        # Get column dtype
        dtype = col.dtype

        # Get distinct values and their counts
        value_counts = col.value_counts()

        # Get number of distinct values
        num_distinct_values = len(value_counts.index)

        # Get min and max values
        sorted_values = sorted(value_counts.index)
        min_value = sorted_values[0] if sorted_values else None
        max_value = sorted_values[-1] if sorted_values else None

        # Get median value
        non_null_values = col.dropna().tolist()
        len_non_null_list = len(non_null_values)

        if len_non_null_list == 0:
            median = None
        else:
            median = non_null_values[len_non_null_list // 2]

        # Get average value if value is number
        if np.issubdtype(dtype, np.number):
            if len_non_null_list > 0:
                avg = sum(non_null_values) / len_non_null_list
                non_zero_avg = (
                    sum([v for v in non_null_values if v > 0]) / len_non_null_list
                )
            else:
                avg = None
                non_zero_avg = None
        else:
            avg = None
            non_zero_avg = None

        # Check if null values are present
        null_present = int(col.isnull().any())

        # Get number of nulls and non-nulls
        num_nulls = col.isnull().sum()
        num_non_nulls = col.notnull().sum()

        # Distinct_values only take top 10 distinct values count
        top_10_d_v = value_counts.head(10).index.tolist()
        top_10_c = value_counts.head(10).tolist()
        top_10_d_v_dict = dict(zip(top_10_d_v, top_10_c))

        # Append the information to the result list
        result.append(
            {
                "col_name": col_name,
                "col_dtype": dtype,
                "num_distinct_values": num_distinct_values,
                "min_value": min_value,
                "max_value": max_value,
                "median_no_na": median,
                "average_no_na": avg,
                "average_non_zero": non_zero_avg,
                "null_present": null_present,
                "nulls_num": num_nulls,
                "non_nulls_num": num_non_nulls,
                "distinct_values": top_10_d_v_dict,
            }
        )

    return pd.DataFrame(result)


def inspect_df(df):
    """
    Print summary information about a Pandas DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame

    Returns:
        None
    """
    print("➡️ df.head()")
    display(df.head(3))
    print("\n➡️ df.shape")
    display(df.shape)

    if df.empty:
        print("\n➡️ df.describe()")
        print("DataFrame is empty; no description available.")
    else:
        print("\n➡️ df.describe()")
        display(df.describe())

    print("\n➡️ NaN Values")
    display(df.isna().sum())
    print(f"\n➡️ Duplicate Rows ➜ {df.duplicated().sum()}")


def univariate_analysis(df):
    # Identify numerical columns
    numerical_columns = df.select_dtypes(include=[np.number]).columns

    # Perform univariate analysis on numerical columns
    for column in numerical_columns:
        # For continuous variables
        if (
            len(df[column].unique()) > 10
        ):  # Assuming if unique values > 10, consider it continuous
            plt.figure(figsize=(8, 6))
            sns.histplot(df[column], kde=True)
            plt.title(f"Histogram of {column}")
            plt.xlabel(column)
            plt.ylabel("Frequency")
            plt.show()
        else:  # For discrete or ordinal variables
            plt.figure(figsize=(8, 6))
            ax = sns.countplot(x=column, data=df)
            plt.title(f"Count of {column}")
            plt.xlabel(column)
            plt.ylabel("Count")

            # Annotate each bar with its count
            for p in ax.patches:
                ax.annotate(
                    format(p.get_height(), ".0f"),
                    (p.get_x() + p.get_width() / 2.0, p.get_height()),
                    ha="center",
                    va="center",
                    xytext=(0, 5),
                    textcoords="offset points",
                )
            plt.show()


def correlation_analysis(df, width=16, height=12):
    """
    Perform correlation analysis on a Pandas DataFrame.

    Parameters:
        df (pd.DataFrame): Input DataFrame
        width (int, optional): Width of the heatmap. Defaults to 16.
        height (int, optional): Height of the heatmap. Defaults to 12.

    Returns:
        None
    """
    numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    categorical_cols = df.select_dtypes(include=["object"]).columns.tolist()

    # Assuming df is your DataFrame
    correlation_matrix = df[numerical_cols].corr()

    # Create the heatmap
    plt.figure(figsize=(width, height))  # Set the size of the plot
    sns.heatmap(correlation_matrix, annot=True, cmap="viridis_r", fmt=".2f")

    # Set title
    plt.title("Correlation Heatmap")

    # Show the plot
    plt.tight_layout()
    plt.show()

    # Find the max correlation
    upper_triangular = correlation_matrix.where(
        np.triu(np.ones(correlation_matrix.shape), k=1).astype(bool)
    )
    max_correlation = upper_triangular.max().max()
    print(f"Maximum pairwise correlation: {max_correlation:.2f}")


def update_column_names(df):
    """
    Updates column names in a Pandas DataFrame by converting them to lower case and replacing spaces with underscores.

    Parameters:
        df (pd.DataFrame): Input DataFrame
    Returns:
        pd.DataFrame: The input DataFrame with updated column names
    """
    df.rename(columns=lambda x: x.lower().replace(" ", "_"), inplace=True)
    return df


def iv_woe(df, target, bins=10, show_woe=False):

    # Empty Dataframe
    newDF, woeDF = pd.DataFrame(), pd.DataFrame()

    # Extract Column Names
    cols = df.columns

    # Run WOE and IV on all the independent variables
    for ivars in cols[~cols.isin([target])]:
        print("Processing variable:", ivars)
        if (df[ivars].dtype.kind in "bifc") and (len(np.unique(df[ivars])) > 10):
            binned_x = pd.qcut(df[ivars], bins, duplicates="drop")
            d0 = pd.DataFrame({"x": binned_x, "y": df[target]})
        else:
            d0 = pd.DataFrame({"x": df[ivars], "y": df[target]})

        # Calculate the number of events in each group (bin)
        d = d0.groupby("x", as_index=False, observed=False).agg({"y": ["count", "sum"]})
        d.columns = ["Cutoff", "N", "Events"]

        # Calculate % of events in each group.
        d["% of Events"] = np.maximum(d["Events"], 0.5) / d["Events"].sum()

        # Calculate the non events in each group.
        d["Non-Events"] = d["N"] - d["Events"]
        # Calculate % of non events in each group.
        d["% of Non-Events"] = np.maximum(d["Non-Events"], 0.5) / d["Non-Events"].sum()

        # Calculate WOE by taking natural log of division of % of non-events and % of events
        d["WoE"] = np.log(d["% of Events"] / d["% of Non-Events"])
        d["IV"] = d["WoE"] * (d["% of Events"] - d["% of Non-Events"])
        d.insert(loc=0, column="Variable", value=ivars)
        print("Information value of " + ivars + " is " + str(round(d["IV"].sum(), 6)))
        temp = pd.DataFrame(
            {"Variable": [ivars], "IV": [d["IV"].sum()]}, columns=["Variable", "IV"]
        )
        newDF = pd.concat([newDF, temp], axis=0)
        woeDF = pd.concat([woeDF, d], axis=0)

        # Show WOE Table
        if show_woe == True:
            print(d)
    return newDF, woeDF


def label_encode_column(df, col_name):
    """
    Label Encode a Column in a Pandas DataFrame.

    Args:
        df (Pandas DataFrame): The input dataframe.
        col_name (str): The name of the column to be encoded.

    Returns:
        Pandas DataFrame: The updated dataframe with the encoded column.
    """

    # Create a LabelEncoder instance
    le = LabelEncoder()

    # Fit and transform the data using the LabelEncoder
    encoded_values = le.fit_transform(df[col_name])

    # Update the dataframe with the encoded column
    df_encoded = pd.DataFrame({col_name: encoded_values})

    df_dropped = df.drop(columns=[col_name])

    return pd.concat([df_dropped, df_encoded], axis=1)


def one_hot_encode_column(df, column_name, drop_original=True):
    """
    One-hot encodes a specified column in the dataframe using sklearn's OneHotEncoder.

    Parameters:
    df (pd.DataFrame): The original dataframe.
    column_name (str): The name of the column to one-hot encode.
    drop_original (bool): Whether to drop the original column after encoding. Default is True.

    Returns:
    pd.DataFrame: A new dataframe with the one-hot encoded columns added.
    """
    # Initialize the OneHotEncoder
    encoder = OneHotEncoder(
        sparse_output=False, drop=None
    )  # sparse_output=False returns a dense array

    # Fit and transform the specified column
    encoded_array = encoder.fit_transform(df[[column_name]])

    # Create a DataFrame with the encoded column names
    encoded_df = pd.DataFrame(
        encoded_array,
        columns=[f"{column_name}_{category}" for category in encoder.categories_[0]],
    )

    # Align index with the original dataframe to avoid any issues
    encoded_df.index = df.index

    # Concatenate the encoded columns with the original dataframe
    df_encoded = pd.concat([df, encoded_df], axis=1)

    # Optionally drop the original column
    if drop_original:
        df_encoded = df_encoded.drop(columns=[column_name])

    return df_encoded


def scale_X_train_X_test(
    X_train, X_test, scaler="standard", save_scaler=False, plot=True
):
    """
    Function to scale the numerical features of a dataframe and plot histograms of scaled features.

    Args:
        X_train (DataFrame): The training dataframe to scale.
        X_test (DataFrame): The test dataframe to scale.
        scaler (str, optional): The type of scaling method to use. Can be 'standard', 'minmax', or 'robust'. Default is 'standard'.
        save_scaler (bool, optional): Whether to save the scaler to disk. Default is False.

    Returns:
        DataFrame: Returns two dataframes with the numerical features scaled (X_train and X_test).
    """
    if scaler == "standard":
        scaler = StandardScaler()
    elif scaler == "minmax":
        scaler = MinMaxScaler()
    elif scaler == "robust":
        scaler = RobustScaler()
    else:
        raise ValueError(
            'Invalid scaler type. Choose "standard", "minmax", or "robust".'
        )

    # Get the column headers
    column_headers = X_train.columns

    # Fit the scaler to the training data and transform both training and test data
    scaled_values_train = scaler.fit_transform(X_train)
    scaled_values_test = scaler.transform(X_test)

    # Convert the transformed data back to a DataFrame, preserving the column headers
    scaled_X_train = pd.DataFrame(scaled_values_train, columns=column_headers)
    scaled_X_test = pd.DataFrame(scaled_values_test, columns=column_headers)

    if save_scaler:
        # Generate a filename with a timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        scaler_filename = f"scaler_{scaler.__class__.__name__}_{timestamp}"

        # Save the scaler to a file
        with open(f"{scaler_filename}.pkl", "wb") as f:
            pickle.dump(scaler, f)

        print(f"💾 Scaler saved to: {scaler_filename}")

    print(
        f"✅ scaled_X_train: fit_transform {scaler.__class__.__name__} - {scaled_X_train.shape}"
    )
    print(
        f"✅ scaled_X_test: transform {scaler.__class__.__name__} - {scaled_X_test.shape}"
    )

    if plot == True:
        # Plot the histograms of the scaled features for training data using seaborn
        plt.figure(figsize=(10, 6))
        sns.histplot(
            scaled_X_train, kde=True, element="step", bins=30, palette="inferno"
        )
        plt.title(
            f"Distribution of Scaled Features in Training Set ({scaler.__class__.__name__})"
        )
        plt.xlabel("Scaled Values")
        plt.ylabel("Frequency")
        plt.show()

        # Plot the histograms of the scaled features for test data using seaborn
        plt.figure(figsize=(10, 6))
        sns.histplot(
            scaled_X_test, kde=True, element="step", bins=30, palette="inferno"
        )
        plt.title(
            f"Distribution of Scaled Features in Test Set ({scaler.__class__.__name__})"
        )
        plt.xlabel("Scaled Values")
        plt.ylabel("Frequency")
        plt.show()

    return scaled_X_train, scaled_X_test


def scale_df(X, scaler="standard", plot=True):
    """
    Function to scale a dataframe using standard or min-max scaling and plot histograms of scaled features.

    Args:
        X (DataFrame): The dataframe to scale.
        scaler (str, optional): The type of scaling method to use. Can be 'standard' or 'minmax'. Default is 'standard'.

    Returns:
        DataFrame: Returns the scaled dataframe.
    """
    if scaler == "standard":
        scaler = StandardScaler()
    elif scaler == "minmax":
        scaler = MinMaxScaler()
    else:
        raise ValueError('Invalid scaler type. Choose "standard" or "minmax".')

    # Fit the scaler to the data and transform the data
    scaled_values = scaler.fit_transform(X)

    # Convert the transformed data back to a DataFrame
    scaled_X = pd.DataFrame(scaled_values, columns=X.columns)

    print(f"✅ X scaled: fit_transform {scaler.__class__.__name__} - {scaled_X.shape}")

    if plot == True:
        # Plot the histograms of the scaled features using seaborn
        plt.figure(figsize=(10, 6))
        sns.histplot(scaled_X, kde=True, element="step", bins=30, palette="inferno")
        plt.title(f"Distribution of Scaled Features ({scaler.__class__.__name__})")
        plt.xlabel("Scaled Values")
        plt.ylabel("Frequency")
        plt.show()

    return scaled_X


def oversample_SMOTE(
    X_train, y_train, sampling_strategy="auto", k_neighbors=5, random_state=42
):
    """
    Oversamples the minority class in the provided DataFrame using the SMOTE (Synthetic Minority Over-sampling Technique) method.

    Parameters:
    ----------
    X_train : Dataframe
        The input DataFrame which contains the features and the target variable.
    y_train : Series
        The name of the column in df that serves as the target variable. This column will be oversampled.
    sampling_strategy : str or float, optional (default='auto')
        The sampling strategy to use. If 'auto', the minority class will be oversampled to have an equal number
        of samples as the majority class. If a float is provided, it represents the desired ratio of the number
        of samples in the minority class over the number of samples in the majority class after resampling.
    k_neighbors : int, optional (default=5)
        The number of nearest neighbors to use when constructing synthetic samples.
    random_state : int, optional (default=0)
        The seed used by the random number generator for reproducibility.

    Returns:
    -------
    X_res : DataFrame
        The features after oversampling.
    y_res : Series
        The target variable after oversampling.

    Example:
    -------
    >>> df = pd.DataFrame({'feature1': np.random.rand(100), 'target': np.random.randint(2, size=100)})
    >>> oversampled_X, oversampled_y = oversample_df(df, 'target', sampling_strategy=0.6, k_neighbors=3, random_state=42)
    """

    # Define the SMOTE instance
    smote = SMOTE(
        sampling_strategy=sampling_strategy,
        k_neighbors=k_neighbors,
        random_state=random_state,
    )

    # Apply the SMOTE method
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    print(
        f"✅ Data Oversampled: SMOTE - X_train:{X_train_res.shape} y_train:{y_train_res.shape}"
    )

    return X_train_res, y_train_res


def define_X_y(df, target):
    target = target

    X = df.drop(columns=target)
    y = df[target]

    print(f"X - independant variables - {X.shape}")
    print(f"y - dependant variable - {target}: {y.shape}")

    return X, y


def train_val_test_split(X, y, val_size=0.2, test_size=0.2, random_state=42):
    # Calculate intermediate size based on test_size
    intermediate_size = 1 - test_size

    # Calculate train_size from intermediate size and validation size
    train_size = 1 - val_size / intermediate_size
    X_train_val, X_test, y_train_val, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_train_val, y_train_val, train_size=train_size, random_state=random_state
    )

    print(f"✅ OUTPUT: X_train, X_val, X_test, y_train, y_val, y_test")
    print(f"Train Set:  X_train, y_train - {X_train.shape}, {y_train.shape}")
    print(f"  Val Set:  X_val, y_val - - - {X_val.shape}, {y_val.shape}")
    print(f" Test Set:  X_test, y_test - - {X_test.shape}, {y_test.shape}")
    return X_train, X_val, X_test, y_train, y_val, y_test


def train_test_split_custom(X, y, test_size=0.2, random_state=42):
    """
    Splits the data into training and testing sets.

    Parameters:
    X (pd.DataFrame or np.ndarray): Features.
    y (pd.Series or np.ndarray): Target variable.
    test_size (float): Proportion of the data to be used as the test set.
    random_state (int): Seed used by the random number generator.

    Returns:
    X_train, X_test, y_train, y_test: Training and testing datasets.
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    print(f"✅ OUTPUT: X_train, X_test, y_train, y_test")
    print(f"Train Set:  X_train, y_train - {X_train.shape}, {y_train.shape}")
    print(f" Test Set:  X_test, y_test - {X_test.shape}, {y_test.shape}")

    return X_train, X_test, y_train, y_test


def sample_df(df, n_samples):
    """
    Samples the input DataFrame.

    Parameters:
    - df: DataFrame. The input DataFrame.
    - n_samples: int. The number of samples to generate.

    Returns:
    - resampled_df: DataFrame. The resampled DataFrame.
    """
    # Error handling: if the number of samples is greater than the DataFrame length.
    if n_samples > len(df):
        print(
            "The number of samples is greater than the number of rows in the dataframe."
        )
        return None
    else:
        sampled_df = df.sample(n_samples, replace=False, random_state=42)
        print(f"Data Sampled: {sampled_df.shape}")
        return sampled_df


def individual_t_test_classification(
    df,
    y_column,
    y_value_1,
    y_value_2,
    list_of_features,
    alpha_val=0.05,
    sample_frac=1.0,
    random_state=None,
):
    """
    Performs individual t-tests for continuous variables between two groups defined by the y_column values.

    Parameters:
    - df: DataFrame. The original DataFrame containing the data.
    - y_column: str. The name of the target column used to split the data into two groups.
    - y_value_1: value. The value of the y_column representing the first group (e.g., 1 for Appointment_status=1).
    - y_value_2: value. The value of the y_column representing the second group (e.g., 0 for Appointment_status=0).
    - list_of_features: list of str. The list of numerical features to perform t-tests on.
    - alpha_val: float. The significance level to determine if the test is significant.
    - sample_frac: float, default=1.0. The fraction of the first group to sample. Set to < 1.0 to sample the first group.
    - random_state: int, default=None. Random state for reproducibility of sampling.

    Returns:
    - df_result: DataFrame. A DataFrame containing the t-statistic, p-value, and significance for each feature.
    """

    # Split the DataFrame into two groups based on y_column values
    group_1 = df[df[y_column] == y_value_1]
    group_2 = df[df[y_column] == y_value_2]

    # Sample the first group if sample_frac is less than 1.0
    if sample_frac < 1.0:
        group_1 = group_1.sample(frac=sample_frac, random_state=random_state)

    new_list = []
    for feature in list_of_features:
        fea_1 = group_1[feature]
        fea_2 = group_2[feature]

        t_stat, p_val = ttest_ind(fea_1, fea_2, equal_var=False)
        t_stat1 = f"{t_stat:.3f}"
        p_val1 = f"{p_val:.3f}"

        if p_val < alpha_val:
            sig = "Significant"
        else:
            sig = "Insignificant"

        new_dict = {
            "feature": feature,
            "t_stat": t_stat1,
            "p_value": p_val1,
            "significance": sig,
        }
        new_list.append(new_dict)

    df_result = pd.DataFrame(new_list)
    return df_result


def individual_t_test_regression(
    df, y_column, list_of_features, alpha_val=0.05, sample_frac=1.0, random_state=None
):
    """
    Performs individual t-tests for continuous variables between two groups defined by the median split of the target column.

    Parameters:
    - df: DataFrame. The original DataFrame containing the data.
    - y_column: str. The name of the target column (continuous variable).
    - list_of_features: list of str. The list of numerical features to perform t-tests on.
    - alpha_val: float. The significance level to determine if the test is significant.
    - sample_frac: float, default=1.0. The fraction of each group to sample. Set to < 1.0 to sample the groups.
    - random_state: int, default=None. Random state for reproducibility of sampling.

    Returns:
    - df_result: DataFrame. A DataFrame containing the t-statistic, p-value, and significance for each feature.
    """

    # Split the DataFrame into two groups based on the median of the y_column
    median_value = df[y_column].median()
    group_1 = df[df[y_column] <= median_value]
    group_2 = df[df[y_column] > median_value]

    # Sample the groups if sample_frac is less than 1.0
    if sample_frac < 1.0:
        group_1 = group_1.sample(frac=sample_frac, random_state=random_state)
        group_2 = group_2.sample(frac=sample_frac, random_state=random_state)

    new_list = []
    for feature in list_of_features:
        fea_1 = group_1[feature]
        fea_2 = group_2[feature]

        t_stat, p_val = ttest_ind(fea_1, fea_2, equal_var=False)
        t_stat1 = f"{t_stat:.3f}"
        p_val1 = f"{p_val:.3f}"

        if p_val < alpha_val:
            sig = "Significant"
        else:
            sig = "Insignificant"

        new_dict = {
            "feature": feature,
            "t_stat": t_stat1,
            "p_value": p_val1,
            "significance": sig,
        }
        new_list.append(new_dict)

    df_result = pd.DataFrame(new_list)
    return df_result


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


from sklearn.metrics import (
    RocCurveDisplay,
    roc_curve,
    auc,
    make_scorer,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
)
from sklearn.model_selection import cross_validate, learning_curve, StratifiedKFold
from sklearn.inspection import permutation_importance
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import label_binarize
from IPython.display import display, HTML
from statsmodels.stats.outliers_influence import variance_inflation_factor


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

    # Determine if the target is binary or multiclass
    n_classes = len(np.unique(y))
    is_multiclass = n_classes > 2

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
    mean_fpr = np.linspace(0, 1, 100)
    tprs = []
    aucs = []

    if is_multiclass:
        y_bin = label_binarize(y, classes=np.unique(y))
        for i, (train, test) in enumerate(cv.split(X, y)):
            model.fit(X.iloc[train], y.iloc[train])
            y_score = model.predict_proba(X.iloc[test])

            for class_idx in range(n_classes):
                fpr, tpr, _ = roc_curve(y_bin[test, class_idx], y_score[:, class_idx])
                tprs.append(np.interp(mean_fpr, fpr, tpr))
                tprs[-1][0] = 0.0
                aucs.append(auc(fpr, tpr))
    else:
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


def best_regression_models(X, y, test_size=0.2, random_state=None, scale_data=False):
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
    for name, model in tqdm(
        models.items(), desc="Testing Regression Models", colour="#9a276b"
    ):
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


def best_classification_models(
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

    # Determine if the target is binary or multiclass
    if len(pd.Series(y).unique()) > 2:
        average_type = "weighted"
        roc_auc_multi_class = "ovr"  # or 'ovo', depending on the use case
    else:
        average_type = "binary"
        roc_auc_multi_class = None  # Not needed for binary classification

    # DataFrame to store results
    results = []

    # Loop over models and evaluate each one with a progress bar
    for name, model in tqdm(
        models.items(), desc="Testing Classification Models", colour="#9a276b"
    ):
        # Create a pipeline if scaling is requested
        if scale_data:
            pipeline = Pipeline([("scaler", StandardScaler()), ("classifier", model)])
            pipeline.fit(X_train, y_train)
            y_pred = pipeline.predict(X_test)
            y_proba = (
                pipeline.predict_proba(X_test)
                if hasattr(pipeline, "predict_proba")
                else None
            )
        else:
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            y_proba = (
                model.predict_proba(X_test) if hasattr(model, "predict_proba") else None
            )

        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        precision = precision_score(y_test, y_pred, average=average_type)
        recall = recall_score(y_test, y_pred, average=average_type)
        f1 = f1_score(y_test, y_pred, average=average_type)

        # Calculate ROC-AUC score appropriately
        if y_proba is not None:
            if roc_auc_multi_class:  # Multiclass case
                roc_auc = roc_auc_score(
                    y_test, y_proba, multi_class=roc_auc_multi_class, average="weighted"
                )
            else:  # Binary case
                roc_auc = (
                    roc_auc_score(y_test, y_proba[:, 1])
                    if y_proba.shape[1] > 1
                    else roc_auc_score(y_test, y_proba)
                )
        else:
            roc_auc = None

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


def plot_elbow_method(scaled_df, k_range=(4, 12), random_state=None):
    """
    Plots the elbow method to find the optimal number of clusters for KMeans clustering.

    Args:
    scaled_df (pd.DataFrame or np.ndarray): The scaled dataframe or array to fit the KMeans model on.
    k_range (tuple): A tuple specifying the range of clusters to try (default is (4, 12)).
    random_state (int, optional): The seed used by the random number generator (default is None).

    Returns:
    None: The function displays a plot showing the elbow method.
    """
    # Instantiate the KMeans model
    model = KMeans(random_state=random_state)

    # Instantiate the KElbowVisualizer with the KMeans model and the specified range for k
    visualizer = KElbowVisualizer(model, k=k_range)

    # Fit the data to the visualizer
    visualizer.fit(scaled_df)

    # Finalize and render the figure
    visualizer.show()


def plot_intercluster_distance(X, n_clusters=6, random_state=None):
    """
    Plots the inter-cluster distances for KMeans clustering.

    Args:
    X (pd.DataFrame or np.ndarray): The data to fit the KMeans model on.
    n_clusters (int): The number of clusters to use in KMeans (default is 6).
    random_state (int, optional): The seed used by the random number generator (default is None).

    Returns:
    None: The function displays a plot showing the inter-cluster distances.
    """
    # Instantiate the KMeans model with the specified number of clusters
    model = KMeans(n_clusters=n_clusters, random_state=random_state)

    # Instantiate the InterclusterDistance visualizer with the KMeans model
    visualizer = InterclusterDistance(model)

    # Fit the data to the visualizer
    visualizer.fit(X)

    # Finalize and render the figure
    visualizer.show()


# Example usage
# plot_intercluster_distance(X, n_clusters=6, random_state=42)

from sklearn.cluster import KMeans
from yellowbrick.cluster import SilhouetteVisualizer


def plot_silhouette_visualizer(X, n_clusters=4, random_state=42, colors="yellowbrick"):
    """
    Plots the silhouette visualizer for KMeans clustering.

    Args:
    X (pd.DataFrame or np.ndarray): The scaled data to fit the KMeans model on.
    n_clusters (int): The number of clusters to use in KMeans (default is 10).
    random_state (int, optional): The seed used by the random number generator (default is 42).
    colors (str or list, optional): The color palette used by Yellowbrick to display the clusters (default is 'yellowbrick').

    Returns:
    None: The function displays a plot showing the silhouette scores for each cluster.
    """
    # Instantiate the KMeans model with the specified number of clusters and random state
    model = KMeans(n_clusters=n_clusters, random_state=random_state)

    # Instantiate the SilhouetteVisualizer with the KMeans model and specified colors
    visualizer = SilhouetteVisualizer(model, colors=colors)

    # Fit the data to the visualizer
    visualizer.fit(X)

    # Finalize and render the figure
    visualizer.show()


# Example usage
# plot_silhouette_visualizer(scaled_X, n_clusters=10, random_state=42, colors='yellowbrick')


def plot_learning_curve(X, y, problem_type="classification", scoring="accuracy"):
    """
    Plots the learning curve for a model based on the type of problem (classification or regression).

    Args:
    X (pd.DataFrame or np.ndarray): The feature data to fit the model on.
    y (pd.Series or np.ndarray): The target variable.
    problem_type (str): The type of problem ('classification' or 'regression'). Default is 'classification'.
    scoring (str): The scoring metric to use for the learning curve. Default is 'accuracy' for classification.

    Returns:
    None: The function displays a learning curve plot.
    """

    # Choose the model based on the problem type
    if problem_type == "classification":
        model = LogisticRegression()
    elif problem_type == "regression":
        model = LinearRegression()
    else:
        raise ValueError(
            "Invalid problem_type. Choose either 'classification' or 'regression'."
        )

    # Plot the learning curve
    learning_curve(model, X, y, scoring=scoring)


# Example usage
# For classification problem
# plot_learning_curve(X, y, problem_type='classification', scoring='accuracy')

# For regression problem
# plot_learning_curve(X, y, problem_type='regression', scoring='r2')


def plot_rfecv(X, y, problem_type="classification", cv_splits=5, scoring="f1_weighted"):
    """
    Plots the Recursive Feature Elimination with Cross-Validation (RFECV) for a model
    based on the type of problem (classification or regression).

    Args:
    X (pd.DataFrame or np.ndarray): The feature data to fit the model on.
    y (pd.Series or np.ndarray): The target variable.
    problem_type (str): The type of problem ('classification' or 'regression'). Default is 'classification'.
    cv_splits (int): Number of cross-validation splits. Default is 5.
    scoring (str): The scoring metric to use for RFECV. Default is 'f1_weighted' for classification.

    Returns:
    None: The function displays an RFECV plot.
    """

    # Choose the model and CV strategy based on the problem type
    if problem_type == "classification":
        model = RandomForestClassifier()
        cv = StratifiedKFold(cv_splits)
        if scoring == "default":
            scoring = "f1_weighted"
    elif problem_type == "regression":
        model = RandomForestRegressor()
        cv = KFold(cv_splits)
        if scoring == "default":
            scoring = "r2"
    else:
        raise ValueError(
            "Invalid problem_type. Choose either 'classification' or 'regression'."
        )

    # Instantiate the RFECV visualizer with the chosen model, CV strategy, and scoring
    visualizer = rfecv(model, X=X, y=y, cv=cv, scoring=scoring)

    # Fit the visualizer
    visualizer.fit(X, y)

    # Finalize and render the figure
    visualizer.show()


# Example usage
# For classification problem
# plot_rfecv(X, y, problem_type='classification', cv_splits=5, scoring='f1_weighted')

# For regression problem
# plot_rfecv(X, y, problem_type='regression', cv_splits=5, scoring='r2')


def impute_values(df, missing_values=0, copy=True, strategy="mean", columns=None):
    """
    Impute specified values in the DataFrame using the provided strategy.

    Parameters:
    - df (DataFrame): The input DataFrame.
    - missing_values (scalar, str, np.nan, or None): The placeholder for the missing values. All occurrences of this
      value will be imputed.
    - copy (bool): If True, a copy of the DataFrame will be created. If False, imputation will be done in-place.
    - strategy (str): The imputation strategy. Options are 'mean', 'median', 'most_frequent', or 'constant'.
    - columns (list): List of column names to apply imputation. If None, all columns will be considered.

    Returns:
    - DataFrame: The DataFrame with imputed values.
    """
    if copy:
        df = df.copy()

    # If columns is None, apply to all columns
    if columns is None:
        columns = df.columns

    # Replace the specified missing values with np.nan
    df[columns] = df[columns].replace(missing_values, np.nan)

    # Create a SimpleImputer with the specified strategy
    imputer = SimpleImputer(missing_values=np.nan, strategy=strategy)

    # Apply the imputer to the specified columns
    df[columns] = imputer.fit_transform(df[columns])

    return df


def remove_outliers_zscore(df, threshold=3):
    """
    Remove outliers from a DataFrame based on the Z-score method.

    Parameters:
    df (pd.DataFrame): The input DataFrame.
    threshold (float): The Z-score threshold to identify outliers (default is 3).

    Returns:
    pd.DataFrame: A DataFrame with outliers removed.
    """
    # Calculate the mean and standard deviation of each column
    mean = df.mean()
    std_dev = df.std()

    # Calculate the Z-scores for each column
    z_scores = (df - mean) / std_dev

    # Filter rows where the absolute Z-score is below the threshold for all columns
    no_outliers_df = df[(np.abs(z_scores) < threshold).all(axis=1)]

    return no_outliers_df


# Example usage:
# Assuming you have a DataFrame named 'train'
# train_no_outliers = remove_outliers_zscore(train)


def impute_missing_values(df, strategy="mean"):
    """
    Fills NaN values in the given DataFrame using the specified strategy.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        strategy (str): The imputation strategy. Options include 'mean', 'median', 'most_frequent', and 'constant'.
                        Default is 'mean'.

    Returns:
        pd.DataFrame: DataFrame with NaN values filled.
    """
    # Create a copy of the dataframe to avoid modifying the original one
    df_imputed = df.copy()

    # Iterate over each column in the dataframe
    for column in df_imputed.columns:
        # Check if the column has missing values
        if df_imputed[column].isnull().sum() > 0:
            # Create a SimpleImputer object with the desired strategy
            imputer = SimpleImputer(strategy=strategy)

            # Reshape the column to 2D array for imputation and fit/transform
            df_imputed[column] = imputer.fit_transform(df_imputed[[column]])

    return df_imputed


def create_qq_plots(df, reference_col):
    """
    Create QQ plots for all features in the DataFrame against a reference column.

    Parameters:
    df (pd.DataFrame): DataFrame containing the features and reference column.
    reference_col (str): The column name of the reference variable (e.g., HbA1c).
    """
    # Ensure the reference column exists in the DataFrame
    if reference_col not in df.columns:
        raise ValueError(f"Reference column '{reference_col}' not found in DataFrame.")

    # Loop through each feature column
    for feature in df.columns:
        if feature == reference_col:
            continue

        # Compute the p-value between the feature and reference column using Pearson correlation
        try:
            corr, p_value = pearsonr(df[feature], df[reference_col])
        except Exception as e:
            print(f"Error computing p-value for {feature}: {e}")
            continue

        # Prepare observed and expected p-values for the QQ plot
        observed_p = [p_value]
        sorted_p = np.sort(observed_p)
        expected = np.linspace(1 / len(sorted_p), 1, len(sorted_p))

        # Generate the QQ plot
        plt.figure(figsize=(6, 5))
        plt.scatter(
            -np.log10(expected),
            -np.log10(sorted_p),
            color="blue",
            alpha=0.6,
            label=f"Observed P-value: {p_value:.4f}",
        )
        plt.plot(
            [0, -np.log10(expected[-1])],
            [0, -np.log10(expected[-1])],
            color="red",
            linestyle="--",
            label="Expected = Observed",
        )
        plt.title(f"QQ Plot: {feature} vs {reference_col}")
        plt.xlabel("Expected -log10(P)")
        plt.ylabel("Observed -log10(P)")
        plt.legend()
        plt.grid(alpha=0.3)
        plt.show()


def volcano_plot(df, reference_col):
    """
    Create a volcano plot of p-values and effect sizes for features in a DataFrame against a reference column.

    Parameters:
    df (pd.DataFrame): DataFrame containing features and a reference column.
    reference_col (str): The column name of the reference variable (e.g., HbA1c).
    """
    # Ensure the reference column exists in the DataFrame
    if reference_col not in df.columns:
        raise ValueError(f"Reference column '{reference_col}' not found in DataFrame.")

    p_values = []
    effect_sizes = []
    features = []

    # Loop through each feature column
    for feature in df.columns:
        if feature == reference_col:
            continue

        try:
            # Drop rows with NaN values in the current feature and reference column
            df_clean = df[[feature, reference_col]].dropna()

            # Calculate Pearson correlation and p-value
            corr, p_value = pearsonr(df_clean[feature], df_clean[reference_col])

            # Store the feature name, p-value, and effect size (correlation as a proxy for effect size)
            features.append(feature)
            p_values.append(p_value)
            effect_sizes.append(corr)
        except ValueError as e:
            print(f"Skipping {feature}: {e}")
            continue

    # Convert results to a DataFrame for plotting
    results_df = pd.DataFrame(
        {"feature": features, "p_value": p_values, "effect_size": effect_sizes}
    )

    # Adjust significance threshold for multiple comparisons (Bonferroni correction)
    significance_threshold = 0.05 / len(features) if features else 0.05

    # Plot the volcano plot
    plt.figure(figsize=(10, 6))
    plt.scatter(
        results_df["effect_size"],
        -np.log10(results_df["p_value"]),
        color="blue",
        alpha=0.7,
        label="Features",
    )
    plt.axhline(
        -np.log10(significance_threshold),
        color="red",
        linestyle="--",
        label=f"P = {significance_threshold:.2e}",
    )
    plt.axvline(0, color="gray", linestyle="--", label="No Effect")
    plt.title("Volcano Plot")
    plt.xlabel("Effect Size (Correlation Coefficient)")
    plt.ylabel("-log10(P-Value)")
    plt.legend()
    plt.grid(alpha=0.3)

    # Annotate significant features
    significant_features = results_df[results_df["p_value"] < significance_threshold]
    for _, row in significant_features.iterrows():
        plt.text(
            row["effect_size"],
            -np.log10(row["p_value"])
            + 0.1,  # Offset the text slightly to avoid overlap
            row["feature"],
            fontsize=8,
            ha="center",
        )

    plt.show()


def check_multicollinearity(df):
    """
    Calculate VIF (Variance Inflation Factor) for each numeric column in the DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame containing features to check.

    Returns:
        pd.DataFrame: A DataFrame with two columns:
            - 'feature': the column names
            - 'VIF': the VIF value for that feature

    Notes:
        - Non-numeric columns are automatically excluded.
        - Rows containing missing values (NaN) are dropped before VIF calculation.
        - A VIF > 5 (or 10, depending on the threshold you adopt) often indicates high multicollinearity.
    """
    # 1) Select only numeric columns and drop rows with NaNs
    numeric_df = df.select_dtypes(include=[np.number]).dropna()

    # 2) Initialize a DataFrame for results
    vif_data = pd.DataFrame()
    vif_data["feature"] = numeric_df.columns

    # 3) Compute VIF for each feature
    vif_data["VIF"] = [
        variance_inflation_factor(numeric_df.values, i)
        for i in range(numeric_df.shape[1])
    ]

    return vif_data
