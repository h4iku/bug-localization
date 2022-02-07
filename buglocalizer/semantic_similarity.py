import json
import pickle

import spacy
import numpy as np
from sklearn.preprocessing import MinMaxScaler

from datasets import DATASET


def calculate_similarity(src_files, bug_reports):

    # Loading word vectors
    nlp = spacy.load('en_core_web_lg')

    src_docs = [nlp(' '.join(src.file_name['unstemmed'] + src.class_names['unstemmed']
                             + src.attributes['unstemmed']
                             + src.comments['unstemmed']
                             + src.method_names['unstemmed']))
                for src in src_files.values()]

    min_max_scaler = MinMaxScaler()

    all_simis = []
    for report in bug_reports.values():
        report_doc = nlp(' '.join(report.summary['unstemmed']
                                  + report.pos_tagged_description['unstemmed']))
        scores = []
        for src_doc in src_docs:
            simi = report_doc.similarity(src_doc)
            scores.append(simi)

        scores = np.array([float(count) for count in scores]).reshape(-1, 1)
        normalized_scores = np.concatenate(
            min_max_scaler.fit_transform(scores)
        )

        all_simis.append(normalized_scores.tolist())

    return all_simis


def main():

    with open(DATASET.root / 'preprocessed_src.pickle', 'rb') as file:
        src_files = pickle.load(file)
    with open(DATASET.root / 'preprocessed_reports.pickle', 'rb') as file:
        bug_reports = pickle.load(file)

    all_simis = calculate_similarity(src_files, bug_reports)

    with open(DATASET.root / 'semantic_similarity.json', 'w') as file:
        json.dump(all_simis, file)


if __name__ == '__main__':
    main()
