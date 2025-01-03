from tqdm import tqdm
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

tqdm.pandas()
import os
import torch.multiprocessing as mp

mp.set_start_method("spawn", force=True)
import pandas as pd
import numpy as np

os.environ["TOKENIZERS_PARALLELISM"] = "false"
import warnings

warnings.filterwarnings("ignore")


sentiment_task = pipeline(
    "sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)


def sentiment_analysis(data, column):
    # Initialize lists to store labels and scores
    sentiment = []
    sentiment_score = []

    # Iterate over DataFrame rows and classify text
    for index, row in tqdm(
        data.iterrows(),
        total=data.shape[0],
        desc="Analyzing Sentiment",
        colour="#e8c44d",
    ):
        freetext = row[column]
        sentence = str(freetext)
        sentence = sentence[:513]
        if pd.isna(sentence) or sentence == "":
            sentiment.append("neutral")
            sentiment_score.append(0)
        else:
            model_output = sentiment_task(sentence)
            sentiment.append(model_output[0]["label"])
            sentiment_score.append(model_output[0]["score"])

    # Add labels and scores as new columns
    data[f"sentiment_{column}"] = sentiment
    data[f"sentiment_score_{column}"] = sentiment_score

    return data
