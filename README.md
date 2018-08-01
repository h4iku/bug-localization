# How to run:
1. Install [Python 3.6+](https://www.python.org/) and required dependencies:
    ```
    pip install xmltodict javalang pygments inflection nltk numpy scipy scikit-learn spacy
    ```
    Also, download and install the GloVe word vectors [`en_vectors_web_lg`](https://spacy.io/models/en#en_vectors_web_lg) for spaCy and [NLTK data](http://www.nltk.org/data.html).

2. Clone this repository:
    ```
    git clone https://github.com/h4iku/bug-localization.git
    ```
    Download the datasets file from [here](http://www.mediafire.com/file/5x0vjnno666ynst/data.zip/file), and unzip it in the root directory of the cloned repository.
    
3. Check the path of datasets in the `datasets.py` module and change the value of the `DATASET` variable to choose different datasets (values can be `aspectj`, `swt`, and `zxing`).
    Run the main module:
    ```
    python main.py
    ```
    All the modules are also independently runnable if it was needed to run them one by one.
