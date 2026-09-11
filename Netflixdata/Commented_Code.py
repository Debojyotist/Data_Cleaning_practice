import pandas as pd

# Load dataset & inspect shape
df = pd.read_csv("netflix_titles.csv")
df.shape

# Peek at the first and last few rows
df.head(3)
df.tail(3)

# View data types and non-null counts
df.info()

# Check for duplicate rows
df.duplicated().sum()

# Check for missing values across columns
df.isna().sum()

# Value counts for categorical columns
df["type"].value_counts(dropna=False)
df["rating"].value_counts(dropna=False)

# Isolate shifted duration values in the rating column
shifted_rows = df[df["rating"].isin(["74 min", "84 min", "66 min"])]
shifted_rows

# Fix misplaced duration values
shift_mask = df["rating"].isin(["74 min", "84 min", "66 min"])
df.loc[shift_mask, "duration"] = df.loc[shift_mask, "rating"]
df.loc[shift_mask, "rating"] = None
df.loc[shift_mask]

# Re-check rating value counts
df["rating"].value_counts(dropna=False)

# Group by type and inspect rating distribution
df.groupby("type")["rating"].value_counts()

# Fill missing rating values with the mode
df["rating"] = df["rating"].fillna(df["rating"].mode()[0])
df["rating"].isna().sum()

# Fill missing text values in categorical columns with 'Unknown'
for column in ["director", "cast", "country"]:
    df[column] = df[column].fillna("Unknown")

df[["director", "cast", "country"]].isna().sum()

# Check titles missing both director and cast
(df["director"] == "Unknown").sum()
((df["director"] == "Unknown") & (df["cast"] == "Unknown")).sum()

# Strip white space and convert 'date_added' to datetime
df["date_added"] = df["date_added"].str.strip()
df["date_added"] = pd.to_datetime(df["date_added"], format="%B %d, %Y")
df["date_added"].head()

# Check missing dates and inspect affected rows
df["date_added"].isna().sum()
df[df["date_added"].isna()]

# Extract year and month features from 'date_added'
df["year_added"] = df["date_added"].dt.year
df["month_added"] = df["date_added"].dt.month
df[["date_added", "year_added", "month_added"]].head()

# Inspect older release years / potential outliers
df[df["release_year"] < 1950][["title", "release_year", "listed_in"]]

# Export clean dataset to Excel and CSV
df.to_excel("netflix_titles_cleaned.xlsx", index=False)
df.to_csv("netflix_titles_cleaned.csv", index=False)