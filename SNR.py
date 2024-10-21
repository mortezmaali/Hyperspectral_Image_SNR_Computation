# -*- coding: utf-8 -*-
"""
Calculate SNR for hyperspectral data using wavelengths

@author: Morteza
"""

import numpy as np
import spectral
import matplotlib.pyplot as plt

# Load your hyperspectral image
input_folder = "C:/Users/Morteza/OneDrive/Desktop/PhD/dataN/Data"
base_name = "Seurat_BEFORE"
header_file = f"{input_folder}/{base_name}.hdr"
spectral_image = spectral.open_image(header_file)

# Access the data as a NumPy array
hyperspectral_data = spectral_image.load()

# Extract wavelengths from the hyperspectral image header
wavelengths = np.array([float(w) for w in spectral_image.metadata['wavelength']])

# Function to calculate SNR per band
def calculate_snr(hyperspectral_data):
    num_bands = hyperspectral_data.shape[2]
    snr_values = []
    
    for i in range(num_bands):
        band_data = hyperspectral_data[:, :, i]
        
        # Mean signal value for the band
        signal_mean = np.mean(band_data)
        
        # Noise estimate: standard deviation of the band data
        noise_std = np.std(band_data)
        
        # SNR calculation
        snr = signal_mean / noise_std if noise_std != 0 else 0
        snr_values.append(snr)
    
    return np.array(snr_values)

# Calculate SNR for all bands
snr_values = calculate_snr(hyperspectral_data)

# Plot SNR values across wavelengths
plt.figure(figsize=(10, 6))
plt.plot(wavelengths, snr_values, marker='o', linestyle='-', color='b')
plt.title('SNR for Each Hyperspectral Band')
plt.xlabel('Wavelength (nm)')
plt.ylabel('SNR')
plt.grid(True)
plt.show()

# Print average SNR across all bands
average_snr = np.mean(snr_values)
print(f"Average SNR across all bands: {average_snr:.2f}")
