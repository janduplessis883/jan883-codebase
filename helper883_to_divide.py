"""
### List of function in `helper883`

1. `scale_df(df, scaler="minmax")`
2. `oversample_SMOTE(X_train, y_train, sampling_strategy="auto", k_neighbors=5, random_state=42)`
3. `evaluate_classification_model(model, X, y, cv=5)`
4. `feature_importance(model, X, y)`
5. `sample_df(df, n_samples)`
6. `automl_tpot(X, y)`
7. `train_val_test_split(X, y, val_size=0.2, test_size=0.2, random_state=42)`
8. `define_X_y(df, target)`
9. `plot_loss_precision_recall_curve(history)`
10. `ask_perplexity(prompt)`
11. `to_markdown(text)`
12. `ask_ollama(user_prompt, model="llama3:8b", format="md", temp="0")`
13. `send_to_notion(subject, content, webhook_url="https://hook.eu1.make.com/cxfkal7tftsbjifdvj6vyiboley1xmld")`
14. `list_functions(module)`
15. `scrape_website(url_list, display_text=False)`
16. `ask_groq(prompt, model="llama3-70b-8192")`
"""

import datetime
import inspect
import json
import os
import time
import warnings

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import seaborn as sns
from bs4 import BeautifulSoup
from groq import Groq
from IPython.display import HTML, Markdown, display
from newsapi import NewsApiClient
from openai import OpenAI
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.inspection import permutation_importance
from sklearn.metrics import (accuracy_score, auc, f1_score, make_scorer,
                             precision_score, recall_score)
# from sklearn.metrics import plot_roc_curve
from sklearn.model_selection import (StratifiedKFold, cross_validate,
                                     learning_curve, train_test_split)
# SKlearn imports
from sklearn.preprocessing import (LabelEncoder, MinMaxScaler, OneHotEncoder,
                                   RobustScaler, StandardScaler)
from tpot import TPOTClassifier

warnings.filterwarnings("ignore")


## Print Welcome Message
def display_message():
    message = "<b>😃 helper883</b> loaded! - run <code>import helper883</code> <code>list_functions(helper883)</code> for a list of functions."
    html_message = f"""
        <span style="color: #345a69; font-size: 12px;">{message}</span>
    """
    display(HTML(html_message))


# Call the function to display the message
display_message()


# functions start here -------------------------------------------------------------------------------------------------
def scale_df(df, scaler="minmax"):
    """
    Function to scale the numerical features of a dataframe.

    Args:
        df (DataFrame): The dataframe to scale.
        scaler (str, optional): The type of scaling method to use. Can be 'standard', 'minmax', or 'robust'. Default is 'minmax'.

    Returns:
        DataFrame: Returns a dataframe with the numerical features scaled.
    """
    if scaler == "standard":
        scaler = StandardScaler()
    elif scaler == "minmax":
        scaler = MinMaxScaler()
    elif scaler == "robust":
        scaler = RobustScaler()
    else:
        raise ValueError('Invalid scaler type. Choose "standard" or "minimax".')

    # Get the column headers
    column_headers = df.columns
    # Fit the scaler to the data and transform the data
    scaled_values = scaler.fit_transform(df)

    # Convert the transformed data back to a DataFrame, preserving the column headers
    scaled_df = pd.DataFrame(scaled_values, columns=column_headers)

    print(f"✅ Data Scaled: {scaler} - {scaled_df.shape}")
    return scaled_df


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
        viz = plot_roc_curve(
            model,
            X.iloc[test],
            y.iloc[test],
            name="ROC fold {}".format(i),
            alpha=0.3,
            lw=1,
            ax=axs[1],
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

    axs[1].plot(
        [0, 1], [0, 1], linestyle="--", lw=2, color="#a10606", label="Chance", alpha=0.6
    )
    axs[1].legend(loc="lower right")
    axs[1].set_title("ROC curve")

    # Show plots
    plt.tight_layout()
    plt.show()


# Permutation feature importance
def feature_importance(model, X, y):
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
        sampled_df = df.sample(n_samples, replace=True, random_state=42)
        print(f"Data Sampled: {sampled_df.shape}")
        return sampled_df


def automl_tpot(X, y):
    # Select features and target
    features = X
    target = y

    # Split the dataset into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2)

    # Create a tpot object with a few generations and population size.
    tpot = TPOTClassifier(
        generations=5, population_size=50, verbosity=2, random_state=42
    )

    # Fit the tpot model on the training data
    tpot.fit(X_train, y_train)

    # Show the final model
    print(tpot.fitted_pipeline_)

    # Use the fitted model to make predictions on the test dataset
    test_predictions = tpot.predict(X_test)

    # Evaluate the model
    print(tpot.score(X_test, y_test))

    # Export the pipeline as a python script file
    time = datetime().now()
    root_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = f"pipelines/tpot_pipeline_{time}.csv"
    output_path = os.path.join(root_dir, output_dir)
    tpot.export(output_path)


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


def define_X_y(df, target):
    target = target

    X = df.drop(columns=target)
    y = df[target]

    print(f"X - independant variable shape: {X.shape}")
    print(f"y - dependant variable - {target}: {y.shape}")

    return X, y


def plot_loss_precision_recall_curve(history):
    fig, ax = plt.subplots(4, 2, figsize=(20, 20), constrained_layout=True)

    # Plot each metric on a separate subplot
    metrics = ["loss", "precision", "recall", "f1_score", "auc", "accuracy"]
    val_metrics = ["val_" + m for m in metrics]
    titles = [
        "Model loss",
        "Model precision",
        "Model recall",
        "Model F1 Score",
        "Model AUC",
        "Model accuracy",
    ]
    y_labels = ["Loss", "Precision", "Recall", "F1 Score", "AUC", "Accuracy"]

    for i, metric in enumerate(metrics):
        ax[i // 2, i % 2].plot(history.history[metric])
        ax[i // 2, i % 2].plot(history.history[val_metrics[i]])
        ax[i // 2, i % 2].set_title(titles[i], fontsize=18)
        ax[i // 2, i % 2].set_ylabel(y_labels[i], fontsize=14)
        ax[i // 2, i % 2].legend(
            ["Train", "Val"], loc="upper left" if "loss" in metric else "lower right"
        )
        ax[i // 2, i % 2].grid(axis="x", linewidth=0.5)
        ax[i // 2, i % 2].grid(axis="y", linewidth=0.5)

    # Learning Rate Plot
    ax[3, 0].plot(history.history["lr"])
    ax[3, 0].set_title("Model Learning Rate", fontsize=18)
    ax[3, 0].set_ylabel("Learning Rate", fontsize=14)
    ax[3, 0].set_xlabel("Epoch", fontsize=14)
    ax[3, 0].grid(axis="x", linewidth=0.5)
    ax[3, 0].grid(axis="y", linewidth=0.5)

    # Remove the empty subplot (if any)
    if len(metrics) % 2 != 0:
        fig.delaxes(ax[3, 1])

    plt.show()


# ------------------------------------------------  Perplexity Chat Endpoint ---
def ask_perplexity(prompt):
    """
    Function to get a chat response from the Perplexity API using the provided prompt.

    Args:
    prompt (str): The prompt to send to the API.

    Returns:
    None: Displays the response content as Markdown.
    """
    # Get the API key from environment variables
    api_key = os.getenv("PERPLEXITY_API_KEY")

    if api_key is None:
        raise ValueError("API key not found in environment variables.")

    # Define the messages
    messages = [
        {
            "role": "system",
            "content": (
                "You are an artificial intelligence assistant and you need to "
                "engage in a helpful, detailed, polite conversation with a user."
            ),
        },
        {
            "role": "user",
            "content": prompt,
        },
    ]

    # Initialize the OpenAI client
    client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")

    # Get the chat completion response
    response = client.chat.completions.create(
        model="llama-3-sonar-large-32k-online",
        messages=messages,
    )
    content = response.choices[0].message.content

    # Display the response content as Markdown
    display(Markdown(content))


# Example usage
# prompt = "Give me an overview of how to connect the make.com API using Python"
# get_chat_response(prompt)


def to_markdown(text):
    """
    Displays the given markdown text using IPython.display.Markdown.

    Parameters:
    text (str): The markdown text to display.
    """
    display(Markdown(text))


def ask_ollama(user_prompt, model="llama3.1", format="text", temp="0"):
    """
    import the following for function to work:
    from helper883 import *
    """

    # Define the endpoint URL and headers
    url = "http://localhost:11434/api/generate"  # Update the URL to match your server's endpoint
    headers = {
        "Content-Type": "application/json",
    }

    # Define the payload with the prompt or input text
    payload = {
        "model": model,  # Replace with your model's name
        "prompt": f"{user_prompt}. output_format={format}",
        "max_tokens": 0,  # Adjust as needed
        "stream": False,
        "temprature": temp,
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # Check the response
    if response.status_code == 200:
        result = response.json()
        return result["response"]
    else:
        print("Error:", response.status_code, response.text)
        return False


def send_to_notion(
    subject,
    content,
    webhook_url="https://hook.eu1.make.com/cxfkal7tftsbjifdvj6vyiboley1xmld",
):
    """
    Sends a webhook with the given subject and content.

    Parameters:
    webhook_url (str): The URL of the webhook to send the payload to.
    subject (str): The subject of the webhook.
    content (str): The content of the webhook.
    """
    # Create the payload
    payload = {"subject": subject, "content": content}

    # Send the POST request to the webhook URL with the payload
    response = requests.post(webhook_url, json=payload)

    # Check the response status
    if response.status_code == 200:
        print("Webhook sent successfully!")
    else:
        print(
            f"Failed to send webhook. Status code: {response.status_code}, Response: {response.text}"
        )


def list_functions(module):
    """
    List all functions in the given module.

    Args:
    - module: The module to inspect.

    Returns:
    - A list of function names in the module.
    """
    functions = inspect.getmembers(module, inspect.isfunction)
    function_names = [function_name for function_name, function in functions]
    return function_names


def scrape_website(url_list, display_text=False):
    cleaned_texts = []

    for url in url_list:
        try:
            # Send a GET request to the webpage
            response = requests.get(url)
            response.raise_for_status()  # Check for request errors

            # Parse the content of the response with BeautifulSoup
            soup = BeautifulSoup(response.content, "html.parser")

            # Extract all text from the webpage
            page_text = soup.get_text()
            text_len = len(page_text.split())
            # Remove all whitespace
            cleaned_text = " ".join(page_text.split())
            cleaned_texts.append(cleaned_text)

            if display_text and cleaned_text:
                print(f"✅ ➔ word count: {text_len}")
                print(cleaned_text)

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while requesting {url}: {e}")
        except Exception as e:
            print(f"An error occurred while processing {url}: {e}")

    return cleaned_texts


def ask_groq(prompt, model="llama3-70b-8192"):
    client = Groq(
        api_key=os.environ.get("GROQ_API_KEY"),
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=model,
    )

    return chat_completion.choices[0].message.content


## update as_groq and ask_ollama with arguments from this function
# def llama_chat(
#     prompts,
#     responses,
#     model="togethercomputer/llama-2-7b-chat",
#     temperature=0.0,
#     max_tokens=0,
#     verbose=False,
#     url=url,
#     headers=headers,
#     base=2,
#     max_tries=3,
# ):

#     prompt = get_prompt_chat(prompts, responses)

#     # Allow multiple attempts to call the API incase of downtime.
#     # Return provided response to user after 3 failed attempts.
#     wait_seconds = [base**i for i in range(max_tries)]

#     for num_tries in range(max_tries):
#         try:
#             response = llama(
#                 prompt=prompt,
#                 add_inst=False,
#                 model=model,
#                 temperature=temperature,
#                 max_tokens=max_tokens,
#                 verbose=verbose,
#                 url=url,
#                 headers=headers,
#             )
#             return response
#         except Exception as e:
#             if response.status_code != 500:
#                 return response.json()

#             print(f"error message: {e}")
#             print(f"response object: {response}")
#             print(f"num_tries {num_tries}")
#             print(
#                 f"Waiting {wait_seconds[num_tries]} seconds before automatically trying again."
#             )
#             time.sleep(wait_seconds[num_tries])

#     print(f"Tried {max_tries} times to make API call to get a valid response object")
#     print("Returning provided response")
#     return response
