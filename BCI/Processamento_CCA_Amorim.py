import numpy as np
import os
import pandas as pd
from scipy.io import loadmat
import matplotlib.pyplot as plt
from scipy import signal
from mne.time_frequency import psd_array_multitaper

# Dicionário para armazenar os dados
original = {}

# Path para o file com os dados
directory = "Data_trials"

# Iterar através de cada pasta de participante
for participant_folder in os.listdir(directory):
    participant_path = os.path.join(directory, participant_folder)
    if os.path.isdir(participant_path):
        participant_number = participant_folder[1:]  # Extrair número do participante do nome da pasta

        # Iterar através dos arquivos MATLAB na pasta do participante
        for file_name in os.listdir(participant_path):
            if file_name.endswith(".mat"):
                file_path = os.path.join(participant_path, file_name)

                # Carregar arquivo MATLAB
                mat_data = loadmat(file_path)

                # Selecionar a key com o nome do file
                keys = mat_data.keys()
                key = list(keys)[3]

                # Criar DataFrame a partir dos dados; .T para transformar linhas em colunas
                df = pd.DataFrame(mat_data[key].T, columns=['TimeStamps','PO3', 'POz', 'PO4', 'O1', 'Oz', 'O2'])

                # Adicionar os dados ao dicionário usando o nome da variável como chave
                if key not in original:
                    original[key] = []
                original[key].append(df)



# Cálculo da frequência de amostragem
data = original['P01_T1_R1_1'][0]
time_diff = data['TimeStamps'].diff().mean()
fs = 1 / time_diff
print("Sampling frequency =", fs, "Hz")



# Definição dos parâmetros do lowpass filter
sos = signal.iirfilter(8, 40, btype='lowpass', analog=False, ftype='butter', fs=fs, output='sos')

#Aplicação de um notch filter para remover frequências de 50 Hz (ruído)
notch_freq = 50.0 
quality_factor = 20.0

b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, fs)

#Dataframe com os dados filtrados
filtrado= {}

#Aplicação do low pass filter
for key, dfs in original.items():
    filtrado[key] = []
    for df in dfs:
        timestamps = df['TimeStamps']
        df_without_timestamps = df.drop(columns=['TimeStamps'])
        df_filtrado = pd.DataFrame(signal.sosfiltfilt(sos, df_without_timestamps.values, axis=0), columns=df_without_timestamps.columns)
        df_filtrado = pd.concat([timestamps, df_filtrado], axis=1)
        filtrado[key].append(df_filtrado)

#Aplicação do notch filter
for key, dfs in filtrado.items():
    for df in dfs:
        for column in df.columns[1:]:
            df[column] = signal.filtfilt(b_notch, a_notch, df[column])

