import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ----------------------
# Load Data
# ----------------------

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
all_topics = set()

for topics in df["topics"].dropna():
    for topic in str(topics).split(","):
        all_topics.add(topic.strip())

# ----------------------
# Topic Weights
# ----------------------

topic_weights = {

    # Very Hard
    "Dynamic Programming": 8,
    "Trie": 7,
    "Segment Tree": 7,
    "Binary Indexed Tree": 7,
    "Suffix Array": 8,
    "Strongly Connected Component": 7,
    "Minimum Spanning Tree": 7,
    "Shortest Path": 7,

    # Hard
    "Graph": 6,
    "Union Find": 6,
    "Topological Sort": 6,
    "Bitmask": 6,
    "Game Theory": 6,
    "Line Sweep": 6,
    "Rolling Hash": 6,
    "Monotonic Queue": 6,

    # Medium-Hard
    "Heap (Priority Queue)": 5,
    "Binary Search": 5,
    "Backtracking": 5,
    "Memoization": 5,
    "String Matching": 5,
    "Eulerian Circuit": 5,
    "Geometry": 5,
    "Probability and Statistics": 5,

    # Medium
    "Tree": 4,
    "Binary Tree": 4,
    "Binary Search Tree": 4,
    "Depth-First Search": 4,
    "Breadth-First Search": 4,
    "Sliding Window": 4,
    "Prefix Sum": 4,
    "Matrix": 4,
    "Ordered Set": 4,
    "Recursion": 4,

    # Easy-Medium
    "Hash Table": 3,
    "Stack": 3,
    "Queue": 3,
    "Linked List": 3,
    "Two Pointers": 3,
    "Greedy": 3,
    "Sorting": 3,
    "Sort": 3,
    "Counting": 3,
    "Simulation": 3,

    # Easy
    "Array": 1,
    "String": 1,
    "Math": 1,
    "Enumeration": 1
}

# ----------------------
# Scoring Function
# ----------------------

def calculate_score(row):

    if row["difficulty"] == "Easy":
        base_score = 15

    elif row["difficulty"] == "Medium":
        base_score = 40

    else:
        base_score = 65

    topic_score = 0

    for topic in str(row["topics"]).split(","):
        topic = topic.strip()
        topic_score += topic_weights.get(topic, 3)

    acceptance_adjustment = (
        (60 - float(row["acceptance_rate"])) * 0.4
    )

    final_score = (
        base_score
        + topic_score
        + acceptance_adjustment
    )

    return round(final_score, 2)

# ----------------------
# Generate Scores
# ----------------------

df["realrank_score"] = df.apply(
    calculate_score,
    axis=1
)

# Normalize to 0-100

min_score = df["realrank_score"].min()
max_score = df["realrank_score"].max()

df["normalized_score"] = (
    (df["realrank_score"] - min_score)
    /
    (max_score - min_score)
) * 100

df["normalized_score"] = (
    df["normalized_score"]
    .round(2)
)
print("\nNORMALIZED SCORE STATS")
print(df["normalized_score"].describe())
# ----------------------
# Difficulty Labels
# ----------------------

def predicted_label(score):

    if score < 25:
        return "Easy"

    elif score < 75:
        return "Medium"

    else:
        return "Hard"


df["realrank_label"] = (
    df["normalized_score"]
    .apply(predicted_label)
)

mismatches = df[
    df["difficulty"] != df["realrank_label"]
]
print("\nREAL RANK DISTRIBUTION")
print(df["realrank_label"].value_counts())

print("\nLEETCODE DISTRIBUTION")
print(df["difficulty"].value_counts())

# ----------------------
# UI
# ----------------------

st.set_page_config(
    page_title="Real Rank",
    page_icon="🚀",
    layout="wide"
)

st.title("🚀 Real Rank")
st.info(
    """
    Real Rank analyzes LeetCode problems using topic complexity,
    acceptance rates, and difficulty labels to estimate practical difficulty.
    """
)

st.markdown(
    "Find the **real difficulty** of LeetCode problems."
)
with st.expander("📖 How Real Rank Works"):

    st.write("""
    Real Rank combines:

    • Official LeetCode difficulty
    • Topic complexity weights
    • Acceptance rate

    to estimate practical difficulty.

    Higher scores indicate harder problems.
    """)
col1, col2, col3 = st.columns(3)

col1.metric("Problems Analyzed", len(df))
col2.metric("Difficulty Mismatches", len(mismatches))
col3.metric("Topics Found", len(all_topics))

# ----------------------
# Search
# ----------------------

search = st.text_input(
    "Search for a LeetCode problem"
)

filtered = df[
    df["title"].str.contains(
        search,
        case=False,
        na=False
    )
]

if len(filtered) == 0:
    st.warning(
        "No matching problems found."
    )
    st.stop()

problem = st.selectbox(
    "Select Problem",
    sorted(filtered["title"].tolist())
)

row = df[
    df["title"] == problem
].iloc[0]

score = row["normalized_score"]

# ----------------------
# Real Rank Label
# ----------------------

if score < 25:
    realrank_label = "Easy"

elif score < 75:
    realrank_label = "Medium"

else:
    realrank_label = "Hard"
# ----------------------
# Breakdown Calculation
# ----------------------

if row["difficulty"] == "Easy":
    base_score = 15

elif row["difficulty"] == "Medium":
    base_score = 40

else:
    base_score = 65

topic_score = 0

for topic in str(row["topics"]).split(","):
    topic = topic.strip()
    topic_score += topic_weights.get(topic, 3)

acceptance_adjustment = (
    (60 - float(row["acceptance_rate"])) * 0.4
)

# ----------------------
# Display Problem Info
# ----------------------

st.subheader(problem)

col1, col2 = st.columns(2)

with col1:

    st.write(
        f"**LeetCode Difficulty:** {row['difficulty']}"
    )

    if realrank_label == "Easy":
        st.success(
            f"Real Rank Difficulty: {realrank_label}"
        )

    elif realrank_label == "Medium":
        st.warning(
            f"Real Rank Difficulty: {realrank_label}"
        )

    else:
        st.error(
            f"Real Rank Difficulty: {realrank_label}"
        )

    st.write(
        f"**Acceptance Rate:** {row['acceptance_rate']}%"
    )

    st.write(
        f"**Topics:** {row['topics']}"
    )
    st.markdown(
    f"[🔗 Open on LeetCode]({row['url']})"
)

with col2:

    st.metric(
        "Real Rank Score",
        f"{score}/100"
    )

# ----------------------
# Score Breakdown
# ----------------------

st.divider()

st.subheader("📊 Score Breakdown")

st.write(
    f"Difficulty Score: {base_score}"
)

st.write(
    f"Topic Complexity Score: {topic_score}"
)

st.write(
    f"Acceptance Adjustment: {round(acceptance_adjustment, 2)}"
)

st.write(
    f"### Final Score: {score}/100"
)

# ----------------------
# Hardest Problems
# ----------------------

st.divider()

st.subheader("🏆 Top 10 Hardest Problems")

top10 = df.sort_values(
    by="normalized_score",
    ascending=False
).head(10)

st.dataframe(
    top10[
        [
            "title",
            "difficulty",
            "normalized_score"
        ]
    ],
    width="stretch"
)

# ----------------------
# Easiest Problems
# ----------------------

st.divider()

st.subheader("😴 Top 10 Easiest Problems")

easy10 = df.sort_values(
    by="normalized_score",
    ascending=True
).head(10)

st.dataframe(
    easy10[
        [
            "title",
            "difficulty",
            "normalized_score"
        ]
    ],
    width="stretch"
)
# ----------------------
# Difficulty Mismatches
# ----------------------

# ----------------------
# Difficulty Mismatches
# ----------------------

st.divider()
hero = mismatches.sort_values(
    by="normalized_score",
    ascending=False
).iloc[0]

st.subheader("⭐ Most Interesting Mismatch")

st.info(
    f"""
    Problem: {hero['title']}

    LeetCode Difficulty: {hero['difficulty']}

    Real Rank Difficulty: {hero['realrank_label']}

    Real Rank Score: {hero['normalized_score']:.2f}
    """
)
st.subheader("🔥 Difficulty Mismatches")

st.write(
    "Problems where Real Rank disagrees with LeetCode."
)

mismatch_display = (
    mismatches[
        [
            "title",
            "difficulty",
            "realrank_label",
            "normalized_score"
        ]
    ]
    .sort_values(
        by="normalized_score",
        ascending=False
    )
    .head(20)
    .rename(
        columns={
            "title": "Problem",
            "difficulty": "LeetCode Difficulty",
            "realrank_label": "Real Rank Difficulty",
            "normalized_score": "Real Rank Score"
        }
    )
)

st.dataframe(
    mismatch_display,
    width="stretch"
)
st.divider()

st.subheader("📈 Real Rank Score Distribution")

fig, ax = plt.subplots()

ax.hist(df["normalized_score"], bins=20)

ax.set_xlabel("Score")
ax.set_ylabel("Number of Problems")

st.pyplot(fig)
easy_mismatches = mismatches[
    mismatches["difficulty"] == "Easy"
]

print("\nEASY MISMATCHES")
print(len(easy_mismatches))

print(
    easy_mismatches[
        ["title",
         "difficulty",
         "realrank_label",
         "normalized_score"]
    ].head(20)
)