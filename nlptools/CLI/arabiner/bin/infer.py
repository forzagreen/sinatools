"""
About:
------
The ArabiNER tool carries out Named Entity Recognition (NER) utilizing the ArabiNER utility from the SinaTools suite. It identifies the named entities and provides a comprehensive analysis in JSON format if the input consists of text, or in a CSV file if the input is a directory of files.

Usage:
------
Below is the usage information that can be generated by running arabi_ner --help.

.. code-block:: none

    arabi_ner --text=INPUT_TEXT
    arabi_ner --dir=INPUT_FILE --output_csv=OUTPUT_FILE_NAME

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

    arabi_ner --text "Your text here"
    arabi_ner --dir "/path/to/your/directory" --output_csv "output.csv"

Note:
-----

.. code-block:: none

    - Ensure that the text input is appropriately encoded in UTF-8 or compatible formats.
    - The tool returns results in JSON format with proper indentation for better readability.
    - The quality and accuracy of the analysis depend on the underlying capabilities of the ArabiNER utility.

"""

import argparse
import json
import pandas as pd
from nlptools.arabiner.bin.infer import ner
from nlptools.utils.corpus_tokenizer import corpus_tokenizer
from nlptools.morphology.tokenizers_words import simple_word_tokenize


def infer(sentence):
    # Now infer returns all NER tags for a sentence
    output = ner(sentence)
    ##print("ner output : ", output)
    return [word[1] for word in output]


def main():
    parser = argparse.ArgumentParser(description='NER Analysis using ArabiNER')

    parser.add_argument('--text', type=str, help='Text to be analyzed for Named Entity Recognition')
    parser.add_argument('--dir', type=str, help='dir containing the text files to be analyzed for Named Entity Recognition')
    parser.add_argument('--output_csv', type=str, help='Output CSV file to write the results')

    args = parser.parse_args()

    if args.text is not None:
        results = ner(args.text)
        # Print the results in JSON format
        print(json.dumps(results, ensure_ascii=False, indent=4))
    elif args.dir is not None:
        corpus_tokenizer(args.dir, args.output_csv)
        df = pd.read_csv(args.output_csv)
        df['NER tags'] = None
        i = 0

        # Use drop_duplicates to get unique values based on Row_ID and Sentence
        result = df.drop_duplicates(subset=['Global Sentence ID', 'Sentence'])
        
        # Get the "Sentence" column as an array
        unique_sentences = result['Sentence'].to_numpy()
        
        # Print the result
        #print(unique_sentences, len(result['Sentence']))
        #print("#############")

        for sentence in unique_sentences:  # iterating over unique sentences            
            #print(" Sentence : ", simple_word_tokenize(sentence), len(simple_word_tokenize(sentence)))
            ner_tags = infer(sentence)  # getting all NER tags for the sentence            
            #if len(ner_tags) != len(df[i:i+len(ner_tags)]):
            #    print("Not Equal...", len(ner_tags) , len(df[i:i+len(ner_tags)]))
            #    return 
            if len(simple_word_tokenize(sentence)) > 300:
                print(" Length of this sentence is more than 300 word:  ", sentence)
                return
            #df['NER tags'].iloc[i:i+len(ner_tags)] = ner_tags
            df.loc[i:i+len(ner_tags)-1, 'NER tags'] = ner_tags  # Use .loc to assign values
            #print("Exit with ner tags = ", ner_tags, " and length : ", len(ner_tags), type(len(ner_tags)), " and df is " , df[i:i+len(ner_tags)], " with length : ", len(df[i:i+len(ner_tags)]), type(len(df[i:i+len(ner_tags)])),  " i:i+len(ner_tags) : ", i," , ", i+len(ner_tags))
            i = i + len(ner_tags)
        
        df.to_csv(args.output_csv, index=False) 
    else:    
        print("Error: Either --text or --file argument must be provided.")
        return


if __name__ == '__main__':
    main()

#arabi_ner --text "Your text here."
#arabi_ner --dir /path/to/your/directory --output_csv output.csv

#Each unique sentence in the CSV file is processed once by the infer function to get the NER tags for all the words in the sentence.
#The current_word_position variable is used to keep track of the position within the list of NER tags returned by infer, ensuring that each word in the CSV file is assigned the correct NER tag.
#The final CSV file will contain an additional column, NER tags, which contains the NER tag for each word in the Sentence column of the CSV file.