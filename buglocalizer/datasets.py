from collections import namedtuple
from pathlib import Path

# Dataset root directory
_DATASET_ROOT = Path('../data')

Dataset = namedtuple('Dataset', ['name', 'root', 'src', 'bug_repo'])

# Source codes and bug repositories
aspectj = Dataset(
    'aspectj',
    _DATASET_ROOT / 'AspectJ',
    _DATASET_ROOT / 'AspectJ/AspectJ-1.5',
    _DATASET_ROOT / 'AspectJ/AspectJBugRepository.xml'
)

swt = Dataset(
    'swt',
    _DATASET_ROOT / 'SWT',
    _DATASET_ROOT / 'SWT/SWT-3.1',
    _DATASET_ROOT / 'SWT/SWTBugRepository.xml'
)

zxing = Dataset(
    'zxing',
    _DATASET_ROOT / 'ZXing',
    _DATASET_ROOT / 'ZXing/ZXing-1.6',
    _DATASET_ROOT / 'ZXing/ZXingBugRepository.xml'
)

### Current dataset in use. (change this name to change the dataset)
DATASET = zxing

if __name__ == '__main__':
    print(DATASET.name, DATASET.root, DATASET.src, DATASET.bug_repo)
