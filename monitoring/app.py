import streamlit as st
import json
import matplotlib.pyplot as plt
import os
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score

# show banner
alert_placeholder = st.empty()

# title and description
st.title('Movie Review Sentiment Monitoring App')
st.markdown("This app will be used to monitor the backend FastAPI application by plotting different data to help in analysing model performance.")

# cache data source only
@st.cache_data
def load_data():
    df = pd.read_csv("IMDB Dataset.csv")
    df["sentence_length"] = df["review"].astype(str).apply(lambda x: len(x.split()))
    return df

# don't cache logs
def load_logs():
    if not os.path.exists("/logs/prediction_logs.json"):
        print("no log file")
        return pd.DataFrame(columns=["sentence_length", "predicted_sentiment", "true_sentiment"])
    
    with open("/logs/prediction_logs.json", "r") as f:
        lines = [json.loads(line) for line in f if line.strip()]

    df = pd.DataFrame(lines)
    if "request_text" in df.columns:
        df["sentence_length"] = df["request_text"].astype(str).apply(lambda x: len(x.split()))
    else:
        df["sentence_length"] = []
    return df

imdb_df = load_data()
log_df = load_logs()

# Data Drift Analysis: Create a histogram or density plot comparing the distribution of sentence lengths from your IMDB Dataset.csv against the lengths from the logged inference requests. 
st.subheader("Sentence Length Distribution Comparison")

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

# IMDB Dataset histogram
ax1.hist(imdb_df["sentence_length"], bins=50, color="skyblue", alpha=0.7)
ax1.set_title("IMDB Dataset Sentence Lengths")
ax1.set_ylabel("Count")
ax1.set_xlim(0, 1000) 

# Log Data histogram
ax2.hist(log_df["sentence_length"], bins=25, color="salmon", alpha=0.7)
ax2.set_title("Predicted Texts (Log Data) Sentence Lengths")
ax2.set_xlabel("Sentence Length (word count)")
ax2.set_ylabel("Count")
ax2.set_xlim(0, 1000) 

# Overall layout
fig.tight_layout()
fig.suptitle("Sentence Length Distribution - IMDB vs Logs", fontsize=14, y=1.02)

st.pyplot(fig)


# Target Drift Analysis: Create a bar chart showing the distribution of predicted sentiments from the logs vs trained sentiments
st.subheader("Target Drift Analysis: Sentiment Distribution")

# Count sentiment labels
data_sentiments = imdb_df["sentiment"].value_counts(normalize=True)
log_sentiments = log_df["predicted_sentiment"].value_counts(normalize=True)

# Combine into a single DataFrame
comparison_df = pd.DataFrame({
    "Trained Sentiments": data_sentiments,
    "Predicted Sentiments": log_sentiments
}).fillna(0)

# Bar chart
comparison_df.plot(kind="bar", figsize=(8, 5))
plt.title("Sentiment Label Distribution: Trained vs Predicted")
plt.ylabel("Proportion")
plt.xticks(rotation=0)
st.pyplot(plt)

# Model Accuracy & User Feedback: From the true_sentiment logged in the logs
# Calculate and display the model's accuracy and precision based on all collected feedback.
st.subheader("Model Accuracy and Precision")

y_true = log_df["true_sentiment"]
y_pred = log_df["predicted_sentiment"]

# compute metrics
accuracy = accuracy_score(y_true, y_pred) if len(y_pred) > 0 else 0
precision = precision_score(y_true, y_pred, pos_label="positive", average="binary", zero_division=0) if len(y_pred) > 0 else 0

# display metrics
st.metric("Accuracy:", f"{accuracy:.2%}")
st.metric("Precision:", f"{precision:.2%}")

# Implement Alerting: If the calculated accuracy drops below 80%, display a prominent warning banner at the top of the dashboard using st.error().
if accuracy < 0.80:
    alert_placeholder.error(f"Warning: Model accuracy dropped to {accuracy:.2%}!", icon="🚨")