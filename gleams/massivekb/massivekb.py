import functools
import itertools
import logging
import os
import subprocess

import joblib
import pandas as pd


logger = logging.getLogger('gleams')


def convert_massivekb_metadata(massivekb_task_id: str) -> None:
    """
    Convert the MassIVE-KB metadata file with the given MassIVE task ID to a
    smaller metadata file containing only the relevant information.
    The initial metadata file needs to be downloaded manually from MassIVE:
    MassIVE Knowledge Base > Human HCD Spectral Library
        > All Candidate library spectra > Download

    The new metadata file will contain PSM information the following columns:
    - dataset: The MassIVE dataset identifier.
    - filename: The file in which the PSM's spectrum is present.
    - scan: The PSM's scan number in its spectral data file.
    - sequence: The PSM's peptide sequence.
    - charge: The PSM's precursor charge.
    - mz: The PSM's precursor m/z.

    This metadata file will be saved to a CSV file
    `metadata_{massivekb_task_id}.csv`.
    If this file already exists it will _not_ be recreated.

    Parameters
    ----------
    massivekb_task_id : str
        The MassIVE task ID corresponding to the downloaded metadata file.
    """
    filename = os.path.join(os.environ['GLEAMS_HOME'], 'data', 'massivekb',
                            f'metadata_{massivekb_task_id}.csv')
    if not os.path.isfile(filename):
        logger.info('Convert the MassIVE-KB metadata file')
        metadata = pd.read_csv(
            os.path.join(os.environ['GLEAMS_HOME'], 'data', 'massivekb',
                         f'LIBRARY_CREATION_AUGMENT_LIBRARY_TEST-'
                         f'{massivekb_task_id}-candidate_library_spectra-'
                         f'main.tsv'),
            sep='\t', usecols=['annotation', 'charge', 'filename', 'mz',
                               'scan'])
        metadata = metadata.rename(columns={'annotation': 'sequence'})
        dataset_filename = metadata['filename'].str.split('/').str
        metadata['dataset'] = dataset_filename[0]
        metadata['filename'] = dataset_filename[-1]
        metadata = metadata.sort_values(['dataset', 'filename', 'scan'])
        logger.debug('Save metadata file to %s', filename)
        metadata.to_csv(filename, index=False)


def download_massive_file(massive_filename: str) -> None:
    """
    Download the given file from MassIVE.

    The file is downloaded using a `wget` subprocess.
    The file will be stored in the `data/peak/{dataset}/{filename}` directory.
    If the file already exists it will _not_ be downloaded again.

    Parameters
    ----------
    massive_filename : str
        The local MassIVE file link.
    """
    dataset = massive_filename.split('/', 1)[0]
    dataset_dir = os.path.join(os.environ['GLEAMS_HOME'], 'data', 'peak',
                               dataset)
    if not os.path.isdir(dataset_dir):
        os.makedirs(dataset_dir)
    peak_filename = massive_filename.rsplit('/', 1)[-1]
    local_filename = os.path.join(dataset_dir, peak_filename)
    if not os.path.isfile(local_filename):
        logger.debug('Download file %s/%s', dataset, peak_filename)
        url = f'ftp://massive.ucsd.edu/{massive_filename}'
        subprocess.run(['wget', '-N', url, '-P', dataset_dir, '-q'])


def download_massivekb_peaks(massivekb_task_id: str) -> None:
    """
    Download all spectral data files listed in the MassIVE-KB metadata file
    with the given MassIVE task ID.

    Peak files will be stored in the `data/peak/{dataset}/{filename}`
    directories.
    Existing peak files will _not_ be downloaded again.

    Parameters
    ----------
    massivekb_task_id : str
        The MassIVE task ID corresponding to the downloaded metadata file.
    """
    filenames = pd.read_csv(
        os.path.join(os.environ['GLEAMS_HOME'], 'data', 'massivekb',
                     f'LIBRARY_CREATION_AUGMENT_LIBRARY_TEST-'
                     f'{massivekb_task_id}-candidate_library_spectra-'
                     f'main.tsv'),
        sep='\t', usecols=['filename'], squeeze=True).unique()
    logger.info('Download peak files from MassIVE')
    joblib.Parallel(n_jobs=-1)(
        joblib.delayed(download_massive_file)(massive_filename)
        for massive_filename in filenames)


def generate_massivekb_pairs_positive(massivekb_task_id: str) -> None:
    """
    Generate index pairs for positive training pairs from the MassIVE-KB
    metadata with the given MassIVE task ID.

    The positive training pairs consist of all pairs with the same peptide
    sequence in the MassIVE-KB metadata. Identity pairs are included.
    Pairs of row numbers in the MassIVE-KB metadata file for each positive pair
    are stored in CSV file `pairs_positive_{massivekb_task_id}.csv`.
    If this file already exists it will _not_ be recreated.

    Parameters
    ----------
    massivekb_task_id : str
        The MassIVE task ID corresponding to the metadata file.
    """
    filename = os.path.join(os.environ['GLEAMS_HOME'], 'data', 'massivekb',
                            f'pairs_positive_{massivekb_task_id}.csv')
    if not os.path.isfile(filename):
        logger.info('Generate MassIVE-KB positive pair indexes')
        metadata = pd.read_csv(os.path.join(
            os.environ['GLEAMS_HOME'], 'data', 'massivekb',
            f'metadata_{massivekb_task_id}.csv'))
        metadata['row_num'] = range(len(metadata.index))
        same_row_nums = metadata.groupby(['sequence', 'charge'],
                                         sort=False)['row_num']
        logger.debug('Save positive pair indexes to %s', filename)
        with open(filename, 'w') as f_out:
            for p1, p2 in itertools.chain(
                    *(same_row_nums.apply(functools.partial(
                        itertools.combinations_with_replacement, r=2)))):
                f_out.write(f'{p1},{p2}\n')


def generate_massivekb_pairs_negative(massivekb_task_id: str,
                                      mz_tolerance: float) -> None:
    """
    Generate index pairs for negative training pairs from the MassIVE-KB
    metadata with the given MassIVE task ID.

    The negative training pairs consist of all pairs with a different peptide
    sequence and a precursor m/z difference smaller than the given m/z
    tolerance in the MassIVE-KB metadata.
    Pairs of row numbers in the MassIVE-KB metadata file for each negative pair
    are stored in CSV file `pairs_negative_{massivekb_task_id}.csv`.
    If this file already exists it will _not_ be recreated.

    Parameters
    ----------
    massivekb_task_id : str
        The MassIVE task ID corresponding to the metadata file.
    mz_tolerance : float
        Maximum precursor m/z tolerance for two PSMs to be considered a
        negative pair.
    """
    filename = os.path.join(os.environ['GLEAMS_HOME'], 'data', 'massivekb',
                            f'pairs_negative_{massivekb_task_id}.csv')
    if not os.path.isfile(filename):
        logger.info('Generate MassIVE-KB negative pair indexes')
        metadata = pd.read_csv(os.path.join(
            os.environ['GLEAMS_HOME'], 'data', 'massivekb',
            f'metadata_{massivekb_task_id}.csv'))
        metadata['row_num'] = range(len(metadata.index))
        metadata = (metadata.sort_values(['charge', 'mz'])
                    .reset_index(drop=True))
        logger.debug('Save negative pair indexes to %s', filename)
        with open(filename, 'w') as f_out:
            for i, (row_num1, peptide1, mz1) in enumerate(zip(
                    metadata['row_num'],
                    metadata['sequence'],
                    metadata['mz'])):
                metadata_next = metadata.iloc[i + 1:]
                for row_num2, peptide2, mz2 in zip(metadata_next['row_num'],
                                                   metadata_next['sequence'],
                                                   metadata_next['mz']):
                    if abs(mz2 - mz1) <= mz_tolerance:
                        if peptide1 != peptide2:
                            f_out.write(f'{row_num1},{row_num2}\n')
                    else:
                        break