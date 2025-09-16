from textblob import TextBlob
import pandas as pd


# user_input = input("Enter usersentiment:  ").lower().strip()
# blob = TextBlob(user_input)

# print(blob.sentiment)

df = pd.read_csv("imdb_top_1000.csv")
print(df.columns)
