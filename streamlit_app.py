import pandas as pd
import streamlit as st

# Load data
df = pd.read_csv("data/Leetcode.csv", header=None)

df.columns = [
    "id",
    "title",
    "difficulty",
    "url",
    "topics",
    "acceptance_rate",
    "premium",
    "category",
    "likes",
    "dislikes",
    "unknown",
    "similar_questions"
]

topic_weights = {
    "Dynamic Programming": 8,
    "Graph": 6,
    "Trie": 7,
    "Heap (Priority Queue)": 5,
    "Union Find": 5,
    "Segment Tree": 7,
    "Binary Indexed Tree": 7,
    "Backtracking": 4,
    "Greedy": 2,
    "Math": 1,
    "Array": 1,
    "String": 1,
    "Hash Table": 2
}

def calculate_score(row):

    if row["difficulty"] == "Easy":
        score = 15
    elif row["difficulty"] == "Medium":
        score = 40
    else:
        score = 65

    topic_score = 0

    for topic in str(row["topics"]).split(","):
        topic = topic.strip()
        topic_score += topic_weights.get(topic, 3)

    score += topic_score

    score += (60 - float(row["acceptance_rate"])) * 0.4

    return round(score, 2)

df["realrank_score"] = df.apply(calculate_score, axis=1)

st.title("Real Rank")

problem = st.selectbox(
    "Select a LeetCode Problem",
    sorted(df["title"].tolist())
)

row = df[df["title"] == problem].iloc[0]

st.subheader(problem)

st.write("LeetCode Difficulty:", row["difficulty"])
st.write("Acceptance Rate:", row["acceptance_rate"])
st.write("Topics:", row["topics"])

st.metric(
    "Real Rank Score",
    row["realrank_score"]
)