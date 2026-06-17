import pandas as pd

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

print("\nDifficulty Distribution:")
print(df["difficulty"].value_counts())

print("\nAcceptance Rate Statistics:")
print(df["acceptance_rate"].describe())

print("\nSample Topics:")
for topic in df["topics"].head(10):
    print(topic)