# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 22:08:11 2024

@author: Morteza
"""

import h5py
import rasterio
import numpy as np

def calculate_snr(signal):
    """
    Calculates the SNR for each band in the hyperspectral image.
    SNR is calculated as the mean of the signal divided by the standard deviation of the noise.
    """
    mean_signal = np.mean(signal, axis=(0, 1))  # Mean across spatial dimensions
    std_noise = np.std(signal, axis=(0, 1))     # Std deviation across spatial dimensions
    snr = mean_signal / std_noise
    return snr

def read_hdf_snr(hdf_file):
    """
    Reads hyperspectral data from an HDF file and calculates the SNR.
    """
    with h5py.File(hdf_file, 'r') as file:
        # Assuming the dataset is named 'hyperspectral_data'; adjust if different
        hyperspectral_data = file['hyperspectral_data'][:]
        snr = calculate_snr(hyperspectral_data)
    return snr

def read_geotiff_snr(geotiff_file):
    """
    Reads hyperspectral data from a GeoTIFF file and calculates the SNR.
    """
    with rasterio.open(geotiff_file) as src:
        # Read all bands into a 3D array (width, height, bands)
        hyperspectral_data = src.read()
        # Rearrange to (height, width, bands) for easier processing
        hyperspectral_data = np.transpose(hyperspectral_data, (1, 2, 0))
        snr = calculate_snr(hyperspectral_data)
    return snr

# Example usage
hdf_file_path = 'path_to_your_L1R_HDF_file.hdf'
geotiff_file_path = 'path_to_your_L1Gst_or_L1T_GeoTIFF_file.tif'

snr_hdf = read_hdf_snr(hdf_file_path)
print("SNR for HDF file:", snr_hdf)

snr_geotiff = read_geotiff_snr(geotiff_file_path)
print("SNR for GeoTIFF file:", snr_geotiff)
