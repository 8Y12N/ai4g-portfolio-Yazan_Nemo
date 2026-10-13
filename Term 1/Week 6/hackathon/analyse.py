import os
import pandas as pd
from transformers import pipeline

POSTS, OUT = "data/posts.csv", "data/sentiment.csv"
MODEL = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

posts = pd.read_csv(POSTS)
done = len(pd.read_csv(OUT)) if os.path.exists(OUT) else 0
new = posts.iloc[done:]  # only posts not analysed yet

if new.empty:
    print("no new posts to analyse")
    raise SystemExit

clf = pipeline("sentiment-analysis", model=MODEL, truncation=True)
results = clf(new["text"].astype(str).tolist(), batch_size=16)

new = new.assign(sentiment=[r["label"].lower() for r in results],
                 score=[round(r["score"], 3) for r in results])
new.to_csv(OUT, mode="a", header=(done == 0), index=False)
print(f"analysed {len(new)} new posts")