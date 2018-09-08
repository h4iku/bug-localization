import pickle
import json
import numpy as np
from sklearn import preprocessing

from datasets import DATASET


def check_matchings(src_files, bug_reports):
    """Checking the matching tokens between bug reports and source files"""
    
    scores = []
    for report in bug_reports.values():
        matched_count = []
        summary_set = report.summary
        pos_tagged_sum_desc = (report.pos_tagged_summary['stemmed'] + 
                               report.pos_tagged_description['stemmed'])
        
        for src in src_files.values():
            if src.file_name['stemmed']:
                common_tokens = len(set(summary_set['stemmed']) & 
                                    set([src.file_name['stemmed'][0]]))

            matched_count.append(common_tokens)

        # Here no files matched a summary
        if sum(matched_count) == 0:
            matched_count = []
            for src in src_files.values():
                common_tokens = len(set(pos_tagged_sum_desc) & 
                                    set(src.file_name['stemmed'] + 
                                        src.class_names['stemmed'] + 
                                        src.method_names['stemmed']))

                if not common_tokens:
                    common_tokens = (len(set(pos_tagged_sum_desc) & 
                                        set(src.comments['stemmed']))
                                     - len(set(src.comments['stemmed'])))
                
                if not common_tokens:
                    common_tokens = (len(set(pos_tagged_sum_desc) & 
                                        set(src.attributes['stemmed']))
                                     - len(set(src.attributes['stemmed'])))
                
                matched_count.append(common_tokens)
        
        min_max_scaler = preprocessing.MinMaxScaler()
        
        intersect_count = np.array([float(count)
                            for count in matched_count]).reshape(-1, 1)
        normalized_count = np.concatenate(
            min_max_scaler.fit_transform(intersect_count)
        )
        
        scores.append(normalized_count.tolist())
        
    return scores


def main():
    
    # Unpickle preprocessed data
    with open(DATASET.root / 'preprocessed_src.pickle', 'rb') as file:
        src_files = pickle.load(file)
    with open(DATASET.root / 'preprocessed_reports.pickle', 'rb') as file:
        bug_reports = pickle.load(file)
        
    scores = check_matchings(src_files, bug_reports)
    
    # Saving scores in a json file
    with open(DATASET.root / 'token_matching.json', 'w') as file:
        json.dump(scores, file)

    
if __name__ == '__main__':
    main()
