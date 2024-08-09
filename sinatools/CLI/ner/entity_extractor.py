"""
About:
------
This tool processes an input text and returns named entites for each token within the text, based on the specified batch size. As follows:

Usage:
------
Below is the usage information that can be generated by running entity_extractor --help.

.. code-block:: none

    entity_extractor --text=INPUT_TEXT
    entity_extractor --dir=INPUT_FILE --output_csv=OUTPUT_FILE_NAME

Options:
--------

.. code-block:: none

  --text INPUT_TEXT
        The text that needs to be analyzed for Named Entity Recognition.
  --file INPUT_FILE
        File containing the text to be analyzed for Named Entity Recognition.
  --output_csv OUTPUT_FILE_NAME
        A file containing the tokenized text and its Named Entity tags.


Examples:
---------

.. code-block:: none

    entity_extractor --text "Your text here"
    entity_extractor --dir "/path/to/your/directory" --output_csv "output.csv"

"""

import argparse
import json
import pandas as pd
from sinatools.ner.entity_extractor import extract
from sinatools.utils.tokenizer import corpus_tokenizer
from sinatools.utils.tokenizers_words import simple_word_tokenize

def jsons_to_list_of_lists(json_list):
    return [[d['token'], d['tags']] for d in json_list]

def combine_tags(sentence):
    output = jsons_to_list_of_lists(extract(sentence, "nested"))
    return [word[1] for word in output]


def main():
    parser = argparse.ArgumentParser(description='NER Analysis using ArabiNER')

    parser.add_argument('--text', type=str, help='Text to be analyzed for Named Entity Recognition')
    parser.add_argument('--dir', type=str, help='dir containing the text files to be analyzed for Named Entity Recognition')
    parser.add_argument('--output_csv', type=str, help='Output CSV file to write the results')

    args = parser.parse_args()

    if args.text is not None:
        results = extract(args.text)
        # Print the results in JSON format
        print(json.dumps(results, ensure_ascii=False, indent=4))
    elif args.dir is not None:
        corpus_tokenizer(args.dir, args.output_csv)
        df = pd.read_csv(args.output_csv)
        df['NER tags'] = None
        i = 0

        result = df.drop_duplicates(subset=['Global Sentence ID', 'Sentence'])
        unique_sentences = result['Sentence'].to_numpy()

        for sentence in unique_sentences: 
            ner_tags = combine_tags(sentence) 
            if len(simple_word_tokenize(sentence)) > 300:
                print(" Length of this sentence is more than 300 word:  ", sentence)
                return
            
            df.loc[i:i+len(ner_tags)-1, 'NER tags'] = ner_tags 
            i = i + len(ner_tags)
        
        df.to_csv(args.output_csv, index=False) 
    else:    
        print("Error: Either --text or --file argument must be provided.")
        return


if __name__ == '__main__':
    main()