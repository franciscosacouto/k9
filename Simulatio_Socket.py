#Libraries
import numpy as np
import os
import pandas as pd
from scipy.io import loadmat
import matplotlib.pyplot as plt
from scipy import signal
from sklearn.cross_decomposition import CCA
import time
import socket


# File path
directory = "Data_trials"

# Dictionary for original data
original = {}

# Window size (seconds)
fs=512
window_seconds = 5
window_size = fs * window_seconds

#Filters parameters
notch_freq = 50.0 
quality_factor = 40.0
highcut = 20
order = 8
lowcut = 5

sos = signal.iirfilter(order, highcut, btype='lowpass', analog=False, ftype='butter', fs=fs, output='sos')
b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, fs)
b_hp, a_hp = signal.butter(order, lowcut, btype='highpass', fs=fs)


#Filters function (Lowpass & HighPass & Notch)
def filter(data):
    filtrado = {}
    for key, dfs in original.items():
        filtrado[key] = []
        for df in dfs:
            timestamps = df['TimeStamps']
            df_without_timestamps = df.drop(columns=['TimeStamps'])
            df_filtrado_lp = pd.DataFrame(signal.sosfiltfilt(sos, df_without_timestamps.values, axis=0), columns=df_without_timestamps.columns)
            df_filtrado_lphp = pd.DataFrame(signal.filtfilt(b_hp, a_hp, df_filtrado_lp.values, axis=0), columns=df_without_timestamps.columns)
            df_filtrado = pd.concat([timestamps, df_filtrado_lphp], axis=1)
            filtrado[key].append(df_filtrado)
    return filtrado

#Channel Oz extraction function
def get_oz(filtrado):
    oz_filtered = {}
    for key, dfs in filtrado.items():
        oz_filtered[key] = []
        for df in dfs:
            oz_filtered_data = df['Oz']
            oz_filtered[key].append(oz_filtered_data)
    return oz_filtered

def get_data(directory):
    for participant_folder in os.listdir(directory):
        participant_path = os.path.join(directory, participant_folder)
        if os.path.isdir(participant_path):
            participant_number = participant_folder[1:]  

            for file_name in os.listdir(participant_path):
                if file_name.endswith(".mat") and not file_name.endswith(("5.mat", "6.mat")):
                    file_path = os.path.join(participant_path, file_name)

                    mat_data = loadmat(file_path)

                    keys = mat_data.keys()
                    key = list(keys)[3]

                    df = pd.DataFrame(mat_data[key].T, columns=['TimeStamps','PO3', 'POz', 'PO4', 'O1', 'Oz', 'O2'])

                    if key not in original:
                        original[key] = []
                    original[key].append(df)

    #Trim data
    num_samples_to_trim = int(0.5 * fs)
    for key, dfs in original.items():
        trimmed_dfs = []
        for df in dfs:
            df_trimmed = df.iloc[num_samples_to_trim:-(num_samples_to_trim)].reset_index(drop=True)
            trimmed_dfs.append(df_trimmed)
        original[key] = trimmed_dfs

    return original

# Correlations function
def calculate_correlations(matrix, reference_signals):
    cca = CCA(n_components=1)  #Canonic components number
    Correlation = []

    for ref_signal in reference_signals:
        cca.fit(matrix, ref_signal)
        x1, x2 = cca.transform(matrix, ref_signal)
        corr = np.corrcoef(x1.T, x2.T)[0, 1]
        Correlation.append(corr)
    
    return Correlation


# Server configuration
SERVER_IP = '127.0.0.1'  # Replace with your server's IP address
SERVER_PORT = 12345      # Replace with your server's port number

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((SERVER_IP, SERVER_PORT))



def simulation(directory,client_socket):
    original = get_data(directory)
    filtered = filter(original)
    oz=get_oz(filtered)

    first_key = list(oz.keys())[0]
    first_matrix = np.array(oz[first_key])
    X = first_matrix.T

    window_size = X.shape[0]
    t = np.linspace(0, 4, window_size, endpoint=False)

    # Generating sine and cosine reference signals
    frequencies = [7, 11, 13, 17]
    reference_signals = []
    for freq in frequencies:
        sine_wave = 10 * np.sin(2 * np.pi * freq * t)
        cosine_wave = 10 * np.cos(2 * np.pi * freq * t)
        reference_signals.append(sine_wave)
        reference_signals.append(cosine_wave)
    
    all_correlations = {}

    for key in oz:
        for data in oz[key]:
            x = np.arange(len(data))/fs
            y = data

        plt.cla()
        plt.plot(x, y, label='Oz')

        plt.legend(loc='upper left')
        plt.tight_layout()
        plt.draw()
        plt.pause(0.05)

        matrix = np.array(oz[key]).T
        correlations = calculate_correlations(matrix, reference_signals)
        max_correlation_index = np.argmax(correlations)
        all_correlations[key] = {'correlations': correlations, 'max_correlation_index': max_correlation_index // 2 + 1}


        client_socket.sendall(str(max_correlation_index // 2 + 1).encode())
        print("Predicted label:", max_correlation_index // 2)
        time.sleep(5)


while True:
    simulation(directory,client_socket)
    time.sleep(5)


