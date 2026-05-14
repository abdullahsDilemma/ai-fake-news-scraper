import pandas as pd
import os

def merge_and_clean_data():
    print("Starting Data Merge and Cleaning Process...\n")
    
    # 1. Load all four raw CSV files
    # Load all four raw CSV files with UTF-8 encoding
    try:
        dawn_df = pd.read_csv('data/dawn_raw.csv', encoding='utf-8')
        guardian_df = pd.read_csv('data/guardian_raw.csv', encoding='utf-8')
        politifact_df = pd.read_csv('data/politifact_raw.csv', encoding='utf-8')
        # We also add 'on_bad_lines' just in case a comma got misplaced inside a quote
        factcheck_df = pd.read_csv('data/factcheck_raw.csv', encoding='utf-8', on_bad_lines='skip')
    except FileNotFoundError as e:
        print(f"Error: Could not find one of the files. {e}")
        return
    # 2. Combine them all together into one massive dataset
    print("1. Combining datasets...")
    master_df = pd.concat([dawn_df, guardian_df, politifact_df, factcheck_df], ignore_index=True)
    print(f"   Total raw articles collected: {len(master_df)}")

    # 3. Clean the data
    print("\n2. Cleaning data...")
    # Drop any rows where the scraper accidentally saved a blank text
    master_df = master_df.dropna(subset=['Headline', 'Article_Text'])
    
    # Drop exact duplicate articles
    master_df = master_df.drop_duplicates(subset=['Headline'])
    print(f"   Total articles after removing duplicates & blanks: {len(master_df)}")

    # 4. Shuffle the data
    print("\n3. Shuffling data like a deck of cards...")
    # frac=1 means 100% of the rows are shuffled. random_state ensures it shuffles the same way if we run it again.
    master_df = master_df.sample(frac=1, random_state=42).reset_index(drop=True)

    # 5. Save the final Master Dataset
    print("\n4. Saving Master Dataset...")
    master_df.to_csv('data/master_dataset.csv', index=False)
    
    # Print the final score!
    print("\n✅ SUCCESS! Final Dataset Distribution:")
    print(master_df['Label'].value_counts())
    print("(Note: 1 = Real News, 0 = Fake News)")

if __name__ == "__main__":
    merge_and_clean_data()