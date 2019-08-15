import abc
import itertools
import logging
import random
from typing import List

import numpy as np
from spectrum_utils.spectrum import MsmsSpectrum

from gleams.embed import spectrum
from gleams.ms_io import ms_io
from gleams.embed import utils

logger = logging.getLogger('gleams')


class SpectrumEncoder(metaclass=abc.ABCMeta):
    """
    Abstract superclass for spectrum encoders.
    """

    feature_names = None

    def __init__(self):
        pass

    @abc.abstractmethod
    def encode(self, spec: MsmsSpectrum) -> np.ndarray:
        """
        Encode the given spectrum.

        Parameters
        ----------
        spec : MsmsSpectrum
            The spectrum to be encoded.

        Returns
        -------
        np.ndarray
            Encoded spectrum features.
        """
        pass


class PrecursorEncoder(SpectrumEncoder):
    """
    Represents a spectrum as precursor features: gray encoding of the precursor
    m/z, gray encoding of the precursor neutral mass, and a one-hot encoding of
    the precursor charge.
    """

    def __init__(self, num_bits_mz: int, mz_min: float, mz_max: float,
                 num_bits_mass: int, mass_min: float, mass_max: float,
                 charge_max: int):
        """
        Instantiate a PrecursorEncoder.

        Parameters
        ----------
        num_bits_mz : int
            The number of bits to use to encode the precursor m/z.
        mz_min : float
            The minimum value between which to scale the precursor m/z.
        mz_max : float
            The maximum value between which to scale the precursor m/z.
        num_bits_mass : int
            The number of bits to use to encode the precursor neutral mass.
        mass_min : float
            The minimum value between which to scale the precursor neutral
            mass.
        mass_max : float
            The maximum value between which to scale the precursor neutral
            mass.
        charge_max : int
            The number of bits to use to encode the precursor charge. Higher
            charges will be clipped to this value.
        """
        super().__init__()

        self.num_bits_mz = num_bits_mz
        self.mz_min = mz_min
        self.mz_max = mz_max
        self.num_bits_mass = num_bits_mass
        self.mass_min = mass_min
        self.mass_max = mass_max
        self.charge_max = charge_max

        self.feature_names = [
            *[f'precursor_mz_{i}' for i in range(self.num_bits_mz)],
            *[f'precursor_mass_{i}' for i in range(self.num_bits_mass)],
            *[f'precursor_charge_{i}' for i in range(self.charge_max)]]

    def encode(self, spec: MsmsSpectrum) -> np.ndarray:
        """
        Encode the precursor of the given spectrum.

        Parameters
        ----------
        spec : MsmsSpectrum
            The spectrum to be encoded.

        Returns
        -------
        np.ndarray
            Spectrum precursor features consisting of: a gray encoding of the
            precursor m/z, a gray encoding of the precursor neutral mass, and
            a one-hot encoding of the precursor charge.
        """
        gray_code_mz = utils.binary_encode(
            spec.precursor_mz, self.mz_min, self.mz_max, self.num_bits_mz)
        precursor_mass = utils.neutral_mass_from_mz_charge(
            spec.precursor_mz, spec.precursor_charge)
        gray_code_mass = utils.binary_encode(
            precursor_mass, self.mass_min, self.mass_max, self.num_bits_mass)
        one_hot_charge = np.zeros((self.charge_max,), np.float32)
        one_hot_charge[min(spec.precursor_charge, self.charge_max) - 1] = 1.
        return np.hstack([gray_code_mz, gray_code_mass, one_hot_charge])


class FragmentEncoder(SpectrumEncoder):
    """
    Represents a spectrum as a vector of fragment ions.
    """

    def __init__(self, min_mz: float, max_mz: float, bin_size: float):
        """
        Instantiate a FragmentEncoder.

        Parameters
        ----------
        min_mz : float
            The minimum m/z to use for spectrum vectorization.
        max_mz : float
            The maximum m/z to use for spectrum vectorization.
        bin_size : float
            The bin size in m/z used to divide the m/z range.
        """
        super().__init__()

        self.min_mz = min_mz
        self.max_mz = max_mz
        self.bin_size = bin_size
        self.num_bins = spectrum.get_num_bins(min_mz, max_mz, bin_size)

        self.feature_names = [f'fragment_bin_{i}'
                              for i in range(self.num_bins)]

    def encode(self, spec: MsmsSpectrum) -> np.ndarray:
        """
        Encode the fragments of the given spectrum.

        Parameters
        ----------
        spec : MsmsSpectrum
            The spectrum to be encoded.

        Returns
        -------
        np.ndarray
            Spectrum fragment features consisting a vector of binned fragments.
        """
        return spectrum.to_vector(spec.mz, spec.intensity, self.min_mz,
                                  self.bin_size, self.num_bins)


class ReferenceSpectraEncoder(SpectrumEncoder):
    """
    Represents a spectrum as similarity to a set of reference spectra.
    """

    def __init__(self, filename: str, min_mz: float, max_mz: float,
                 fragment_mz_tol: float, num_ref_spectra: int):
        """
        Instantiate a ReferenceSpectraEncoder by vectorizing the reference
        spectra in the given file.

        Parameters
        ----------
        filename : str
            The file from which to read the reference spectra.
        min_mz : float
            The minimum m/z to include in the vector.
        max_mz : float
            The maximum m/z to include in the vector.
        fragment_mz_tol : float
            The fragment m/z tolerance used to compute the spectrum dot
            product to the reference spectra.
        num_ref_spectra : int
            Maximum number of reference spectra to consider. An error is raised
            if this exceeds the number of available reference spectra.
        """
        super().__init__()

        self.fragment_mz_tol = fragment_mz_tol

        logger.debug('Read the reference spectra')
        ref_spectra = list(ms_io.get_spectra(filename))
        if len(ref_spectra) < num_ref_spectra:
            raise ValueError(f'Insufficient number of reference spectra '
                             f'({len(ref_spectra)} available, '
                             f'{num_ref_spectra} required)')
        elif len(ref_spectra) > num_ref_spectra:
            logger.debug('Select %d reference spectra (was %d)',
                         len(ref_spectra), num_ref_spectra)
            ref_spectra = random.sample(ref_spectra, num_ref_spectra)
        logger.debug('Vectorize the reference spectra')
        self.ref_spectra = [spec for spec in ref_spectra
                            if (spectrum.preprocess(spec, min_mz, max_mz)
                                .is_valid)]

        self.feature_names = [f'ref_{i}' for i in range(len(ref_spectra))]

    def encode(self, spec: MsmsSpectrum) -> np.ndarray:
        """
        Encode the given spectrum by its similarity with a set of reference
        spectra.

        Parameters
        ----------
        spec : MsmsSpectrum
            The spectrum to be encoded.

        Returns
        -------
        np.ndarray
            Reference spectrum features consisting of the spectrum's dot
            product similarity to a set of reference spectra.
        """
        return np.asarray([spectrum.dot(ref.mz, ref.intensity, spec.mz,
                                        spec.intensity, self.fragment_mz_tol)
                           for ref in self.ref_spectra])


class MultipleEncoder(SpectrumEncoder):
    """
    Combines multiple child encoders.
    """

    def __init__(self, encoders: List[SpectrumEncoder]):
        """
        Instantiate a MultipleEncoder with the given child encoders.

        Parameters
        ----------
        encoders : List[SpectrumEncoder]
            The child encoders to do the actual spectrum encoding.
        """
        super().__init__()

        self.encoders = encoders

        self.feature_names = list(itertools.chain.from_iterable(
            [enc.feature_names for enc in self.encoders]))

    def encode(self, spec: MsmsSpectrum) -> np.ndarray:
        """
        Encode the given spectrum using the child encoders.

        Parameters
        ----------
        spec : MsmsSpectrum
            The spectrum to be encoded.

        Returns
        -------
        np.ndarray
            Concatenated spectrum features produced by all child encoders.
        """
        return np.hstack([enc.encode(spec) for enc in self.encoders])
