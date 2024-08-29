"""
About:
------
The implication tool evaluates the implication between two words using the functionalities provided by the `Implication` class of SinaTools. This tool can be utilized to determine the relationship between two words and understand if one implies the other.

Usage:
------
Below is the usage information that can be generated by running implication --help.

.. code-block:: none

    Usage:
        implication --inputWord1=WORD1 --inputWord2=WORD2
        
        implication --inputFile1=File1 --inputFile2=File2  

.. code-block:: none

    Options:
      --inputWord1 WORD1
            First input word.

      --inputWord2 WORD2
            Second input word.

      --file1 FILE1
            File containing the words to evaluate the implication.

      --file2 FILE2
            File containing the words to evaluate the implication.
Examples:
---------

.. code-block:: none

      implication --inputWord1 "word1" --inputWord2 "word2"
      
      implication --file1 "path/to/your/file1.txt" --file2 "path/to/your/file2.txt"

"""
import argparse
from sinatools.utils.word_compare import Implication

def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        word = file.readline().strip()
        if word:
            return word
        else:
            raise ValueError(f"File {file_path} must contain at least one word.")

def main():
    parser = argparse.ArgumentParser(description='Evaluate Implication between two words using SinaTools')
    
    # Adding optional arguments for the two input words and the files
    parser.add_argument('--inputWord1', type=str, help='First input word')
    parser.add_argument('--inputWord2', type=str, help='Second input word')
    parser.add_argument('--file1', type=str, help='File containing the first word to evaluate implication')
    parser.add_argument('--file2', type=str, help='File containing the second word to evaluate implication')

    args = parser.parse_args()

    if args.file1 and args.file2:
        word1 = read_file(args.file1)
        word2 = read_file(args.file2)
    elif args.inputWord1 and args.inputWord2:
        word1, word2 = args.inputWord1, args.inputWord2
    else:
        print("Either --file1 and --file2 arguments or both --inputWord1 and --inputWord2 arguments must be provided.")
        return

    # Instantiate the Implication class
    implication_obj = Implication(word1, word2)
    
    # For this example, assuming there is a method `get_verdict()` in the Implication class.
    result = implication_obj.get_verdict()
    print(result)

if __name__ == '__main__':
    main()
# implication --inputWord1 "word1" --inputWord2 "word2"
# implication --file1 "path/to/your/firstfile.txt" --file2 "path/to/your/secondfile.txt"


