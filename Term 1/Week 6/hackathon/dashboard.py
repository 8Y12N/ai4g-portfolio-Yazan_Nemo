import pandas as pd
import streamlit as st

URL = ("https://raw.githubusercontent.com/8Y12N/ai4g-portfolio-Yazan_Nemo/main/"
       "Term%201/Week%206/hackathon/data/sentiment.csv")
ALARM = 3  # negative/neutral outage posts in one hour = alarm

st.set_page_config(page_title="Outage Pulse", layout="wide")
st.title("Outage Pulse")
st.caption("Mood of public Bluesky posts about outages of cloud, platform and Dutch internet services. "
           "⚠️ Small, noisy sample: always check the posts behind a peak before acting.")

@st.cache_data(ttl=300)  # fetch fresh data from GitHub at most every 5 min
def load():
    df = pd.read_csv(URL, parse_dates=["time_utc"])
    df["hour"] = df["time_utc"].dt.floor("h")
    return df

df = load()

# filter per service (e.g. to hide noisy ones like "teams")
all_services = sorted(df["service"].unique())
picked = st.sidebar.multiselect("Services", all_services, default=all_services)
df = df[df["service"].isin(picked)]
if df.empty:
    st.info("No posts yet.")
    st.stop()

# key numbers, with post counts so nobody trusts a % based on 2 posts
last24 = df[df["time_utc"] > df["time_utc"].max() - pd.Timedelta(hours=24)]
c1, c2, c3 = st.columns(3)
c1.metric("Posts collected", len(df))
c2.metric("Posts last 24h", len(last24))
c3.metric("Negative share last 24h", f"{(last24['sentiment'] == 'negative').mean():.0%}")

# chart: posts per hour, split by sentiment
st.subheader("Outage posts per hour")
per_hour = (df.pivot_table(index="hour", columns="sentiment", values="text",
                           aggfunc="count", fill_value=0)
              .reindex(columns=["negative", "neutral", "positive"], fill_value=0))
st.bar_chart(per_hour, color=["#d62728", "#999999", "#2ca02c"])

alarm = per_hour[(per_hour["negative"] + per_hour["neutral"]) >= ALARM]
if not alarm.empty:
    st.error(f"🚨 {len(alarm)} hour(s) with {ALARM}+ negative/neutral outage posts")

# drill down: the posts behind a peak
st.subheader("What's behind a peak?")
totals = per_hour.sum(axis=1).sort_values(ascending=False)
pick = st.selectbox("Pick an hour (busiest first)", totals.index,
                    format_func=lambda h: f"{h:%d %b %H:00} UTC ({totals[h]} posts)")
st.dataframe(df[df["hour"] == pick][["time_utc", "service", "sentiment", "score", "text"]],
             use_container_width=True, hide_index=True)