# **jan883-codebase** - EDA and Model Selection Toolkit

This repository contains a collection of Python functions designed to streamline Exploratory Data Analysis (EDA) and model selection processes. The toolkit is divided into three main sections: **EDA Level 1**, **EDA Level 2**, and **Model Selection**, each providing a set of utility functions to assist in data transformation, analysis, and model evaluation.

## Package Content

### **EDA Level 1 — Transformation of Original Data**
This section focuses on the initial transformation and cleaning of raw data. Key functionalities include:
- **Column Name Standardization**: Convert column names to lowercase and replace spaces with underscores.
- **Handling Missing Values**: Fill null/NaN values with appropriate data.
- **Data Type Conversion**: Ensure columns have the correct data types.
- **Data Validation**: Validate the integrity of the dataset.
- **Categorical Feature Mapping/Binning**: Map or bin categorical features for better analysis.
- **Encoding**: Perform Label Encoding and One-Hot Encoding on categorical columns.
- **Outlier Removal**: Remove outliers using Z-score.
- **Imputation**: Impute missing values using strategies like median, mean, or mode.

### **EDA Level 2 — Understanding of Transformed Data**
This section delves deeper into understanding the transformed data through advanced analysis techniques:
- **Correlation Analysis**: Generate correlation heatmaps and identify maximum pairwise correlations.
- **IV/WOE Analysis**: Calculate Information Value (IV) and Weight of Evidence (WOE) to assess feature predictive power.
- **Feature Importance**: Extract feature importance from models.
- **Statistical Tests**: Perform individual t-tests for classification and regression problems.
- **QQ Plots**: Create QQ plots for feature comparison.
- **Data Scaling**: Scale data for exploration or model training.
- **Train-Test Splitting**: Split data into training, validation, and test sets.
- **Oversampling**: Use SMOTE to oversample minority classes.

### **Model Selection — Choosing the Right Model**
This section provides tools for evaluating and selecting the best models for your data:
- **Feature Importance Visualization**: Plot feature importance for a given model.
- **Learning Curves**: Generate learning curves for regression and classification models.
- **Recursive Feature Elimination**: Perform recursive feature elimination with cross-validation.
- **Model Evaluation**: Evaluate classification and regression models using key metrics.
- **Best Model Selection**: Test multiple regression and classification models to identify the best-performing one.
- **Clustering Analysis**: Use the Elbow Method, Intercluster Distance, and Silhouette Visualizer to determine optimal clustering parameters.

## Key Features
- **Custom Functions**: Pre-built functions for common EDA and model selection tasks.
- **Modular Design**: Functions are designed to be reusable and adaptable to different datasets.
- **Visualization**: Integrated visualization tools for better data understanding and model evaluation.

This toolkit is ideal for data scientists and analysts looking to accelerate their EDA and model selection workflows. Whether you're working on classification, regression, or clustering tasks, this repository provides the tools to make your process more efficient and insightful.
