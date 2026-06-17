import pandas as pd

# Load dataset
df = pd.read_csv("data/Leetcode.csv", header=None)

# Column names
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

# Topic difficulty weights
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

    # Topic complexity
    topic_score = 0

    for topic in str(row["topics"]).split(","):
        topic = topic.strip()
        topic_score += topic_weights.get(topic, 3)

    score += topic_score

    # Acceptance rate
    acceptance_bonus = (60 - float(row["acceptance_rate"])) * 0.4
    score += acceptance_bonus

    return round(score, 2)
# Generate scores
df["realrank_score"] = df.apply(calculate_score, axis=1)

# Sort by score
top20 = df.sort_values(
    by="realrank_score",
    ascending=False
)

print("\nTOP 20 HARDEST PROBLEMS ACCORDING TO REAL RANK:\n")

print(
    top20[
        [
            "title",
            "difficulty",
            "acceptance_rate",
            "topics",
            "realrank_score"
        ]
    ].head(20)
)

print("\nSCORE DISTRIBUTION:\n")
print(df["realrank_score"].describe())
print("\nEASIEST PROBLEMS:\n")

print(
    df.sort_values(
        by="realrank_score",
        ascending=True
    )[
        [
            "title",
            "difficulty",
            "acceptance_rate",
            "topics",
            "realrank_score"
        ]
    ].head(20)
)