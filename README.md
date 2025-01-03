# **jan883-codebase** - Data Science Collection
![jan883_codebase logo](images/logo2.png)

This repository contains a collection of Python functions designed to streamline Exploratory Data Analysis (EDA) and model selection processes. The toolkit is divided into three main sections: **EDA Level 1**, **EDA Level 2**, **Model Selection** and a selection of other tools lick **NotionHelper**, helper class for the Official Notio API via `notion-client` each providing a set of utility functions to assist in data transformation, analysis, and model evaluation.

This toolkit is ideal for data scientists and analysts looking to accelerate their EDA and model selection workflows. Whether you're working on classification, regression, or clustering tasks, this repository provides the tools to make your process more efficient and insightful.

---
# Data Pre-processing
```python
from jan883_codebase.data_preprocessing.eda import *

# Run this function for a printout of included functions in Jupyter Notebook.
eda0()
eda1()
eda2()
```
### **EDA Level 0 - Pure Understanding of Original Data**

- `inspect_df(df) Run df.head()`, df.describe(), df.isna().sum() & df.duplicated().sum() on your dataframe.
- `column_summary(df)` Create a dataframe with column info, dtype, value_counts, etc.
- `column_summary_plus(df)` Create a dataframe with column info, dtype, value_counts, plus df.decsribe() info.
- `univariate_analysis(df)` Perform Univariate Analysis of numeric columns.

### **EDA Level 1 — Transformation of Original Data**

- `update_column_names(df)` Update Column names, replace " " with "_".
- `label_encode_column(df, col_name)` Label encode a df column returing a df with the new column (original col dropped).
- `one_hot_encode_column(df, col_name)` One Hot Encode a df column returing a df with the new column (original col dropped).
- `train_no_outliers = remove_outliers_zscore(train, threshold=3)` Remove outliers using Z score.
- `df_imputed = impute_missing_values(df, strategy='median')` Impute missing values in DF

### **EDA Level 2 — Understanding of Transformed Data**
- `correlation_analysis(df, width=16, height=12)` Correlation Heatmap & Maximum pairwise correlation.
- `newDF, woeDF = iv_woe(df, target, bins=10, show_woe=False)` Returns newDF, woeDF. IV / WOE Values - Information Value (IV) quantifies the prediction power of a feature. We are looking for IV of 0.1 to 0.5. For those with IV of 0, there is a high chance it is the way it is due to imbalance of data, resulting in lack of binning. Keep this in mind during further analysis.
- `individual_t_test_classification(df, y_column, y_value_1, y_value_2, list_of_features, alpha_val=0.05, sample_frac=1.0, random_state=None)` Statistical test of individual features - Classification problem.
- `individual_t_test_regression(df, y_column, list_of_features, alpha_val=0.05, sample_frac=1.0, random_state=None)` Statistical test of individual features - Regressions problem.
- `create_qq_plots(df, reference_col)` Create QQ plots of the features in a dataframe.
- `volcano_plot(df, reference_col)` Create Volcano Plot with P-values.
- `X, y = define_X_y(df, target)` Define X and y..
- `X_train, X_test, y_train, y_test = train_test_split_custom(X, y, test_size=0.2, random_state=42)` Split train, test.
- `X_train, X_val, X_test, y_train, y_val, y_test = train_val_test_split(X, y, val_size=0.2, test_size=0.2, random_state=42)` Split train, val, test.
- `X_train_res, y_train_res = oversample_SMOTE(X_train, y_train, sampling_strategy="auto", k_neighbors=5, random_state=42) `Oversample minority class.
- `scaled_X = scale_df(X, scaler='standard')` only scales X, does not scale X_test or X_val.
- `scaled_X_train, scaled_X_test = scale_X_train_X_test(X_train, X_test, scaler="standard", save_scaler=False)` Standard, MinMax and Robust Scaler. X_train uses fit_transform, X_test uses transform.
- `sample_df(df, n_samples)` Take a sample of the full df.
---
# Model Selection
```python
from jan883_codebase.data_preprocessing.eda import *

ml0() # Run this function for a printout of included functions in Jupyter Notebook.
```

- `feature_importance_plot(model, X, y)` Plot Feature Importance using a single model.
- `evaluate_classification_model(model, X, y, cv=5)` Plot peformance metrics of single classification model.
- `evaluate_regression_model(model, X, y)` Plot peformance metrics of single regression model.
- `test_regression_models(X, y, test_size=0.2, random_state=None, scale_data=False)` Test Regression models.
- `test_classification_models(X, y, test_size=0.2, random_state=None, scale_data=False)` Test Classification models.
---
# NotionHelper class

```python
import os
# Set the environment variable
os.environ["NOTION_TOKEN"] = "<your-notion-token>"

from jan883_codebase.notion_api.notionhelper import NotionHelper
nh = NotionHelper() # Instantiate the class

nh.get_all_pages_as_dataframe(database_id)
```
A helper class to interact with the **Notion API.**

### Methods

- `get_database(database_id)`: Fetches the schema of a Notion database given its database_id.
- `notion_search_db(database_id, query="")`: Searches for pages in a Notion database that contain the specified query in their title.
- `notion_get_page(page_id)`: Returns the JSON of the page properties and an array of blocks on a Notion page given its page_id.
- `create_database(parent_page_id, database_title, properties)`: Creates a new database in Notion under the specified parent page with the given title and properties.
- `new_page_to_db(database_id, page_properties)`: Adds a new page to a Notion database with the specified properties.
- `append_page_body(page_id, blocks)`: Appends blocks of text to the body of a Notion page.
- `get_all_page_ids(database_id)`: Returns the IDs of all pages in a given Notion database.
- `get_all_pages_as_json(database_id, limit=None)`: Returns a list of JSON objects representing all pages in the given database, with all properties.
- `get_all_pages_as_dataframe(database_id, limit=None)`: Returns a Pandas DataFrame representing all pages in the given database, with selected properties.
---
# More function:
NER, RAG, Semitment Analysis, Telegram API, Web Scrapping Tools
