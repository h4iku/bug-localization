# How to run:
1. Install [Python 3.8+](https://www.python.org/) and clone this repository:
    ```
    git clone https://github.com/h4iku/bug-localization.git
    ```

2. Create a venv and install the dependencies:
    ```
    cd bug-localization
    python -m venv env
    ./env/Scripts/activate
    pip install -r requirements.txt
    ```
    Also, download and install the spaCy's [`en_core_web_lg`](https://spacy.io/models/en#en_core_web_lg) pretrain model and [NLTK data](http://www.nltk.org/data.html).
    
3. Download the datasets file from [here](http://www.mediafire.com/file/5x0vjnno666ynst/data.zip/file), and unzip it in the root directory of the cloned repository.
    
4. Check the path of datasets in `buglocalizer/datasets.py` module and change the value of the `DATASET` variable to choose different datasets (values can be `aspectj`, `swt`, and `zxing`).
    
    Run the main module:
    ```
    python buglocalizer/main.py
    ```
    All the modules are also independently runnable if it was needed to run them one by one.
