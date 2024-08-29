"""

About:
------
The corpus_tokenizer command offers functionality to tokenize a corpus and write the results to a CSV file. It recursively searches through a specified directory for text files, tokenizes the content, and outputs the results, including various metadata, to a specified CSV file.

Usage:
-------
Below is the usage information that can be generated by running corpus_tokenizer --help.

.. code-block:: none

    Usage:
        corpus_tokenizer dir_path output_csv

.. code-block:: none
    dir_path
        The path to the directory containing the text files.

    output_csv
        The path to the output CSV file.

Examples:
---------
.. code-block:: none
    corpus_tokenizer --dir_path "/path/to/text/directory/of/files" --output_csv  "outputFile.csv"
"""

import argparse
from sinatools.utils.tokenizer import corpus_tokenizer

# Define the main function that will parse the arguments
def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description='Tokenize the corpus and write the results to a CSV file.')
    
    # Add arguments to the parser
    parser.add_argument('--dir_path', type=str, help='The path to the directory containing the text files.')
    parser.add_argument('--output_csv', type=str, help='The path to the output CSV file.')
    
    # Parse the command-line arguments
    args = parser.parse_args()
    
    # Call the corpus_tokenizer function with the parsed arguments
    corpus_tokenizer(args.dir_path, args.output_csv)

# Call the main function when the script is executed
if __name__ == '__main__':
    main()

