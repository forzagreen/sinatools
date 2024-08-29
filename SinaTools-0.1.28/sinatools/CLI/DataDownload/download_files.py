"""
About:
------

The download_files command, allows users to select specific files and models to download and use it within SinaTools modules. Additionally, it automatically manages the extraction of compressed files, including zip and tar.gz formats.

Usage:
------

Below is the usage information that can be generated by running download_files --help.

.. code-block:: none

    Usage:
     download_files [OPTIONS]

.. code-block:: none

        Options:
        -f, --files FILES
            Names of the files to download. Available files are: ner, morph, wsd, synonyms. 
            If no file is specified, all files will be downloaded.

Examples:
---------

.. code-block:: none

    download_files -f morph ner 
    This command will download only the `morph` and `ner` files to the default directory.
"""

import argparse
from sinatools.DataDownload.downloader import download_file
from sinatools.DataDownload.downloader import download_files
from sinatools.DataDownload.downloader import get_appdatadir
from sinatools.DataDownload.downloader import urls


def main():
    parser = argparse.ArgumentParser(description="Download files from specified URLs.")
    parser.add_argument('-f', '--files', nargs="*",
                        help="Names of the files to download. Available files are: "
                             f"{', '.join(urls.keys())}. If no file is specified, all files will be downloaded.")
    
    get_appdatadir()

    args = parser.parse_args()

    if args.files:
        for file in args.files:
            print("file: ", file)
            if file == "wsd":
                download_file(urls["morph"])
                download_file(urls["ner"])
                download_file(urls["wsd_model"])
                download_file(urls["wsd_tokenizer"])
                download_file(urls["one_gram"])
                download_file(urls["five_grams"])
                download_file(urls["four_grams"])
                download_file(urls["three_grams"])
                download_file(urls["two_grams"])
            elif file == "synonyms":
                download_file(urls["graph_l2"])
                download_file(urls["graph_l3"])
            else:
               url = urls[file]
               download_file(url)
    else:
        download_files()

if __name__ == '__main__':
    main()
