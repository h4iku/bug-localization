import preprocessing
import vsm_similarity
import token_matching
import stack_trace
import semantic_similarity
import fixed_bug_reports
import evaluation

print('Parsing & Preprocessing...')
preprocessing.main()

print('Token Matching...')
token_matching.main()

print('VSM Similarity...')
vsm_similarity.main()

print('Stack Trace...')
stack_trace.main()

print('Semantic Similarity...')
semantic_similarity.main()

print('Fixed Bug Reports...')
fixed_bug_reports.main()

print('Evaluating...')
evaluation.main()