import re
import pandas as pd
from rouge_score import rouge_scorer



def paragraph_to_sentences(paragraph):
    # Split the paragraph into sentences using regular expressions
    # Split the paragraph into sentences using sentence delimiters.
    sentences = re.split(r"(?<=[\.!\?])\s+", paragraph)


    #print("Sentences == " , sentences)

    # Remove any leading or trailing whitespace from each sentence.
    sentences = [sentence.strip(".?!") for sentence in sentences if sentence]
    low = []
    for sentence in sentences:
        print("S == ", sentence)
        [low.append(word) for word in sentence.split()]
    print(low)
    return low

def convert_file_to_df():
    # Specify the path to your Excel file
    file_path = "RougeExampleSheet.xlsx"  # Replace with your actual file path

    # Read the Excel sheet using pandas.read_excel()
    try:
        df = pd.read_excel(file_path)
    except FileNotFoundError:
        print("Error: Excel file not found. Please check the file path.")
    else:
        print("Excel sheet imported successfully!")
        # Now you can work with the DataFrame 'df'
        # For example, print the first few rows
        print(df.head())
    return df

def process_df_rouge(df):
    R1P = []
    R1R = []
    R1F1 = []
    R2P = []
    R2R = []
    R2F1 = []
    RLP = []
    RLR = []
    RLF1 = []
    for index, row in df.iterrows():
        # Access the value of the 'column_name' column for the current row
        gs = row['Gold Standard']
        rs = row['Reference Summary']
        # Do something with the value (e.g., print it)
        print(f"Row index: {index}, GS: {gs}, RS: {rs}")
        scores = calculate_rouge(gs, rs)

        for key in scores:
            print(f'{key}: {scores[key]}')
            #print("scores === ", scores['rouge1'].recall)
            if key == "rouge1":
                R1P.append(scores['rouge1'].precision)
                R1R.append(scores['rouge1'].recall)
                R1F1.append(scores['rouge1'].fmeasure)
            if key == "rouge2":
                R2P.append(scores['rouge2'].precision)
                R2R.append(scores['rouge2'].recall)
                R2F1.append(scores['rouge2'].fmeasure)
            if key == "rougeL":
                RLP.append(scores['rougeL'].precision)
                RLR.append(scores['rougeL'].recall)
                RLF1.append(scores['rougeL'].fmeasure)

        print("rouge collect = ", R1P,R2R, RLF1)
    df['R1P'] = R1P
    df['R1R'] = R1R
    df['R1F1'] = R1F1
    df['R2P'] = R2P
    df['R2R'] = R2R
    df['R2F1'] = R2F1
    df['RLP'] = RLP
    df['RLR'] = RLR
    df['RLF1'] = RLF1
    print(df)

    file_name = "RougeScoreResults.xlsx"
    df.to_excel(file_name, index=False)  # Optional: index=False to exclude the row index

    print(f"Data successfully exported to Excel file: {file_name}")
def calculate_rouge(cs_gs,rs):
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(rs, cs_gs)
    return scores


# Example usage
if __name__ == "__main__":
    #paragraph = "This is a sample paragraph.  Must i'll funny It contains multiple sentences. Here is another sentence with a question mark? Finally, one more sentence with an exclamation mark!"

    # words_list = paragraph_to_sentences(paragraph)
    # print(words_list)
    df = convert_file_to_df()
    process_df_rouge(df)
