import string
import pickle
import re

import inflection
import nltk
from nltk.stem.porter import PorterStemmer

from assets import stop_words, java_keywords
from parsers import Parser

from datasets import DATASET


class ReportPreprocessing:
    """Class to preprocess bug reports"""
    
    __slots__ = ['bug_reports']
    
    def __init__(self, bug_reports):
        self.bug_reports = bug_reports
    
    def extract_stack_traces(self):
        """Extracting stack traces from bug reports"""
        
        # Simple pattern to retrieve stack traces
        pattern = re.compile(r' at (.*?)\((.*?)\)')
        
        # Signs of a true stack trace to check in the retrieved regex grouping
        signs = ['.java', 'Unknown Source', 'Native Method']

        for report in self.bug_reports.values():
            st_candid = re.findall(pattern, report.description)
            
            # Filter actual stack traces from retrieved candidates
            st = [x for x in st_candid if any(s in x[1] for s in signs)]
            report.stack_traces = st
    
    def pos_tagging(self):
        """Extracing specific pos tags from bug reports' summary and description"""
        
        for report in self.bug_reports.values():
            
            # Tokenizing using word_tokeize for more accurate pos-tagging
            summ_tok = nltk.word_tokenize(report.summary)
            desc_tok = nltk.word_tokenize(report.description)
            sum_pos = nltk.pos_tag(summ_tok)
            desc_pos = nltk.pos_tag(desc_tok)
            
            report.pos_tagged_summary = [token for token, pos in sum_pos
                                         if 'NN' in pos or 'VB' in pos]
            report.pos_tagged_description = [token for token, pos in desc_pos
                                             if 'NN' in pos or 'VB' in pos]
        
    def tokenize(self):
        """Tokenizing bug reports into tokens"""
        
        for report in self.bug_reports.values():
            report.summary = nltk.wordpunct_tokenize(report.summary)
            report.description = nltk.wordpunct_tokenize(report.description)
    
    def _split_camelcase(self, tokens):
    
        # Copy tokens
        returning_tokens = tokens[:]
        
        for token in tokens:
            split_tokens = re.split(fr'[{string.punctuation}]+', token)
            
            # If token is split into some other tokens
            if len(split_tokens) > 1:
                returning_tokens.remove(token)
                # Camel case detection for new tokens
                for st in split_tokens:
                    camel_split = inflection.underscore(st).split('_')
                    if len(camel_split) > 1:
                        returning_tokens.append(st)
                        returning_tokens += camel_split
                    else:
                        returning_tokens.append(st)
            else:
                camel_split = inflection.underscore(token).split('_')
                if len(camel_split) > 1:
                    returning_tokens += camel_split
    
        return returning_tokens
    
    def split_camelcase(self):
        """Split CamelCase identifiers"""
        
        for report in self.bug_reports.values():
            report.summary = self._split_camelcase(report.summary)
            report.description = self._split_camelcase(report.description)
            report.pos_tagged_summary = self._split_camelcase(report.pos_tagged_summary)
            report.pos_tagged_description = self._split_camelcase(report.pos_tagged_description)
            
    def normalize(self):
        """Removing punctuation, numbers and also lowercase conversion"""
        
        # Building a translate table for punctuation and number removal
        punctnum_table = str.maketrans({c : None for c in string.punctuation + string.digits})
        
        for report in self.bug_reports.values():
            summary_punctnum_rem = [token.translate(punctnum_table)
                                    for token in report.summary]
            desc_punctnum_rem = [token.translate(punctnum_table)
                                 for token in report.description]
            pos_sum_punctnum_rem = [token.translate(punctnum_table)
                                  for token in report.pos_tagged_summary]
            pos_desc_punctnum_rem = [token.translate(punctnum_table)
                                  for token in report.pos_tagged_description]
            
            report.summary = [token.lower() for token
                              in summary_punctnum_rem if token]
            report.description = [token.lower() for token
                                  in desc_punctnum_rem if token]
            report.pos_tagged_summary = [token.lower() for token
                                         in pos_sum_punctnum_rem if token]
            report.pos_tagged_description = [token.lower() for token
                                             in pos_desc_punctnum_rem if token]
            
    def remove_stopwords(self):
        """Removing stop words from tokens"""
        
        for report in self.bug_reports.values():
            report.summary = [token for token in report.summary
                              if token not in stop_words]
            report.description = [token for token in report.description
                                  if token not in stop_words]
            report.pos_tagged_summary = [token for token in report.pos_tagged_summary
                                         if token not in stop_words]
            report.pos_tagged_description = [token for token in report.pos_tagged_description
                                             if token not in stop_words]
            
    def remove_java_keywords(self):
        """Removing Java language keywords from tokens"""

        for report in self.bug_reports.values():
            report.summary = [token for token in report.summary
                              if token not in java_keywords]
            report.description = [token for token in report.description
                                  if token not in java_keywords]
            report.pos_tagged_summary = [token for token in report.pos_tagged_summary
                                         if token not in java_keywords]
            report.pos_tagged_description = [token for token in report.pos_tagged_description
                                             if token not in java_keywords]
    
    def stem(self):
        """Stemming tokens"""
        
        # Stemmer instance
        stemmer = PorterStemmer()

        for report in self.bug_reports.values():
            report.summary = dict(zip(['stemmed', 'unstemmed'],
                                      [[stemmer.stem(token) for token in report.summary],
                                       report.summary]))
            
            report.description = dict(zip(['stemmed', 'unstemmed'],
                                          [[stemmer.stem(token) for token in report.description],
                                           report.description]))
            
            report.pos_tagged_summary = dict(zip(['stemmed', 'unstemmed'],
                                                 [[stemmer.stem(token) for token
                                                   in report.pos_tagged_summary],
                                                  report.pos_tagged_summary]))
            
            report.pos_tagged_description = dict(zip(['stemmed', 'unstemmed'],
                                                     [[stemmer.stem(token) for token
                                                       in report.pos_tagged_description],
                                                      report.pos_tagged_description]))

    def preprocess(self):
        """Run the preprocessing"""
        
        self.extract_stack_traces()
        self.pos_tagging()
        self.tokenize()
        self.split_camelcase()
        self.normalize()
        self.remove_stopwords()
        self.remove_java_keywords()
        self.stem()
        

class SrcPreprocessing:
    """Class to preprocess source codes"""
    
    __slots__ = ['src_files']
    
    def __init__(self, src_files):
        self.src_files = src_files
    
    def pos_tagging(self):
        """Extracing specific pos tags from comments"""
        
        for src in self.src_files.values():
            
            # Tokenizing using word_tokeize for more accurate pos-tagging
            comments_tok = nltk.word_tokenize(src.comments)
            comments_pos = nltk.pos_tag(comments_tok)
             
            src.pos_tagged_comments = [token for token, pos in comments_pos
                                       if 'NN' in pos or 'VB' in pos]
    
    def tokenize(self):
        """Tokenizing source codes into tokens"""
        
        for src in self.src_files.values():
            src.all_content = nltk.wordpunct_tokenize(src.all_content)
            src.comments = nltk.wordpunct_tokenize(src.comments)
    
    def _split_camelcase(self, tokens):
    
        # Copy tokens
        returning_tokens = tokens[:]
        
        for token in tokens:
            split_tokens = re.split(fr'[{string.punctuation}]+', token)
            
            # If token is split into some other tokens
            if len(split_tokens) > 1:
                returning_tokens.remove(token)
                # Camel case detection for new tokens
                for st in split_tokens:
                    camel_split = inflection.underscore(st).split('_')
                    if len(camel_split) > 1:
                        returning_tokens.append(st)
                        returning_tokens += camel_split
                    else:
                        returning_tokens.append(st)
            else:
                camel_split = inflection.underscore(token).split('_')
                if len(camel_split) > 1:
                    returning_tokens += camel_split
    
        return returning_tokens
    
    def split_camelcase(self):
        """Split CamelCase identifiers"""
        
        for src in self.src_files.values():
            src.all_content = self._split_camelcase(src.all_content)
            src.comments = self._split_camelcase(src.comments)
            src.class_names = self._split_camelcase(src.class_names)
            src.attributes = self._split_camelcase(src.attributes)
            src.method_names = self._split_camelcase(src.method_names)
            src.variables = self._split_camelcase(src.variables)
            src.file_name = self._split_camelcase(src.file_name)
            src.pos_tagged_comments = self._split_camelcase(src.pos_tagged_comments)
            
    def normalize(self):
        """Removing punctuation, numbers and also lowercase conversion"""
        
        # Building a translate table for punctuation and number removal
        punctnum_table = str.maketrans({c : None for c in string.punctuation + string.digits})
        
        for src in self.src_files.values():
            content_punctnum_rem = [token.translate(punctnum_table)
                                    for token in src.all_content]
            comments_punctnum_rem = [token.translate(punctnum_table)
                                     for token in src.comments]
            classnames_punctnum_rem = [token.translate(punctnum_table)
                                       for token in src.class_names]
            attributes_punctnum_rem = [token.translate(punctnum_table)
                                       for token in src.attributes]
            methodnames_punctnum_rem = [token.translate(punctnum_table)
                                        for token in src.method_names]
            variables_punctnum_rem = [token.translate(punctnum_table)
                                      for token in src.variables]
            filename_punctnum_rem = [token.translate(punctnum_table)
                                     for token in src.file_name]
            pos_comments_punctnum_rem = [token.translate(punctnum_table)
                                         for token in src.pos_tagged_comments]
            
            src.all_content = [token.lower() for token
                               in content_punctnum_rem if token]
            src.comments = [token.lower() for token
                            in comments_punctnum_rem if token]
            src.class_names = [token.lower() for token
                               in classnames_punctnum_rem if token]
            src.attributes = [token.lower() for token
                              in attributes_punctnum_rem if token]
            src.method_names = [token.lower() for token
                                in methodnames_punctnum_rem if token]
            src.variables = [token.lower() for token
                             in variables_punctnum_rem if token]
            src.file_name = [token.lower() for token
                             in filename_punctnum_rem if token]
            src.pos_tagged_comments = [token.lower() for token
                                       in pos_comments_punctnum_rem if token]
            
    def remove_stopwords(self):
        """Removing stop words from tokens"""
        
        for src in self.src_files.values():
            src.all_content = [token for token in src.all_content
                               if token not in stop_words]
            src.comments = [token for token in src.comments
                            if token not in stop_words]
            src.class_names = [token for token in src.class_names
                               if token not in stop_words]
            src.attributes = [token for token in src.attributes
                              if token not in stop_words]
            src.method_names = [token for token in src.method_names
                                if token not in stop_words]
            src.variables = [token for token in src.variables
                             if token not in stop_words]
            src.file_name = [token for token in src.file_name
                             if token not in stop_words]
            src.pos_tagged_comments = [token for token in src.pos_tagged_comments
                                       if token not in stop_words]
            
    def remove_java_keywords(self):
        """Removing Java language keywords from tokens"""

        for src in self.src_files.values():
            src.all_content = [token for token in src.all_content
                               if token not in java_keywords]
            src.comments = [token for token in src.comments
                            if token not in java_keywords]
            src.class_names = [token for token in src.class_names
                               if token not in java_keywords]
            src.attributes = [token for token in src.attributes
                              if token not in java_keywords]
            src.method_names = [token for token in src.method_names
                                if token not in java_keywords]
            src.variables = [token for token in src.variables
                             if token not in java_keywords]
            src.file_name = [token for token in src.file_name
                             if token not in java_keywords]
            src.pos_tagged_comments = [token for token in src.pos_tagged_comments
                                       if token not in java_keywords]
    
    def stem(self):
        """Stemming tokens"""
        
        # Stemmer instance
        stemmer = PorterStemmer()
        
        for src in self.src_files.values():
            src.all_content = dict(zip(['stemmed', 'unstemmed'],
                                       [[stemmer.stem(token) for token in src.all_content],
                                        src.all_content]))
            
            src.comments = dict(zip(['stemmed', 'unstemmed'],
                                    [[stemmer.stem(token) for token in src.comments],
                                     src.comments]))
            
            src.class_names = dict(zip(['stemmed', 'unstemmed'],
                                       [[stemmer.stem(token) for token in src.class_names],
                                        src.class_names]))
            
            src.attributes = dict(zip(['stemmed', 'unstemmed'],
                                      [[stemmer.stem(token) for token in src.attributes],
                                       src.attributes]))
            
            src.method_names = dict(zip(['stemmed', 'unstemmed'],
                                        [[stemmer.stem(token) for token in src.method_names],
                                         src.method_names]))
            
            src.variables = dict(zip(['stemmed', 'unstemmed'],
                                     [[stemmer.stem(token) for token in src.variables],
                                      src.variables]))
            
            src.file_name = dict(zip(['stemmed', 'unstemmed'],
                                     [[stemmer.stem(token) for token in src.file_name],
                                      src.file_name]))
            
            src.pos_tagged_comments = dict(zip(['stemmed', 'unstemmed'],
                                      [[stemmer.stem(token) for token in src.pos_tagged_comments],
                                       src.pos_tagged_comments]))

    def preprocess(self):
        """Run the preprocessing"""
        
        self.pos_tagging()
        self.tokenize()        
        self.split_camelcase()
        self.normalize()
        self.remove_stopwords()
        self.remove_java_keywords()
        self.stem()
            

def main():
    
    parser = Parser(DATASET)
    
    src_prep = SrcPreprocessing(parser.src_parser())
    src_prep.preprocess()
    with open(DATASET.root / 'preprocessed_src.pickle', 'wb') as file:
        pickle.dump(src_prep.src_files, file, protocol=pickle.HIGHEST_PROTOCOL)
    
    report_prep = ReportPreprocessing(parser.report_parser())
    report_prep.preprocess()
    with open(DATASET.root / 'preprocessed_reports.pickle', 'wb') as file:
        pickle.dump(report_prep.bug_reports, file, protocol=pickle.HIGHEST_PROTOCOL)

    
if __name__ == '__main__':
    main()
