#Importação das bibliotecas
import numpy as np
import os
import pandas as pd
from scipy.io import loadmat
import matplotlib.pyplot as plt
from scipy import signal
from sklearn.cross_decomposition import CCA
import time


# Path para o file com os dados
directory = "Data_trials"

# Dicionário para armazenar a raw EEG
original = {}

# Tamanho da window em segundos
fs=512
window_seconds = 5
window_size = fs * window_seconds

#frequências dos estímulos
frequencies = [7, 11, 13, 17]

#Função para aplicar filtros (Lowpass & HighPass & Notch)
def filter(data):
    #Definição de parâmetros dos filtros
    notch_freq = 50.0 
    quality_factor = 40.0
    highcut = 20
    order = 8
    lowcut = 5

    sos = signal.iirfilter(order, highcut, btype='lowpass', analog=False, ftype='butter', fs=fs, output='sos')
    b_notch, a_notch = signal.iirnotch(notch_freq, quality_factor, fs)
    b_hp, a_hp = signal.butter(order, lowcut, btype='highpass', fs=fs)

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

#Função para extrair dados do canal Oz
def get_oz(filtrado):
    oz_filtered = {}
    for key, dfs in filtrado.items():
        oz_filtered[key] = []
        for df in dfs:
            oz_filtered_data = df['Oz']
            oz_filtered[key].append(oz_filtered_data)
    return oz_filtered

def get_data(directory):
    # Iterar através de cada pasta de participante
    for participant_folder in os.listdir(directory):
        participant_path = os.path.join(directory, participant_folder)
        if os.path.isdir(participant_path):
            participant_number = participant_folder[1:]  # Extrair número do participante do nome da pasta

            # Iterar através dos arquivos MATLAB na pasta do participante
            for file_name in os.listdir(participant_path):
                if file_name.endswith(".mat") and not file_name.endswith(("5.mat", "6.mat")):
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
    
    #Tirar o primeiro e último meio segundo de cada amostra
    num_samples_to_trim = int(0.5 * fs)
    for key, dfs in original.items():
        trimmed_dfs = []
        for df in dfs:
            df_trimmed = df.iloc[num_samples_to_trim:-(num_samples_to_trim)].reset_index(drop=True)
            trimmed_dfs.append(df_trimmed)
        original[key] = trimmed_dfs

    return original

# Função para calcular as correlações
def calculate_correlations(matrix, reference_signals):
    cca = CCA(n_components=1)  #número de componentes canônicos
    Correlation = []

    for ref_signal in reference_signals:
        cca.fit(matrix, ref_signal)
        x1, x2 = cca.transform(matrix, ref_signal)
        corr = np.corrcoef(x1.T, x2.T)[0, 1]
        Correlation.append(corr)
    
    return Correlation

def generate_ref(frequencies, data):
    #Extrair primeiro dado para definir legth das referências
    first_key = list(data.keys())[0]
    first_matrix = np.array(data[first_key])
    X = first_matrix.T

    window_size = X.shape[0]
    t = np.linspace(0, 4, window_size, endpoint=False)

    # Gerar sinais de referência com seno e cosseno
    frequencies = [7, 11, 13, 17]
    reference_signals = []
    for freq in frequencies:
        sine_wave = 10 * np.sin(2 * np.pi * freq * t)
        cosine_wave = 10 * np.cos(2 * np.pi * freq * t)
        reference_signals.append(sine_wave)
        reference_signals.append(cosine_wave)
    
    return reference_signals

#Simulação
def simulation(directory):
    original = get_data(directory)
    filtered = filter(original)
    oz=get_oz(filtered)
    reference = generate_ref(frequencies,oz)

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
        correlations = calculate_correlations(matrix, reference)
        max_correlation_index = np.argmax(correlations)  # Índice da coluna com o valor máximo
        all_correlations[key] = {'correlations': correlations, 'max_correlation_index': max_correlation_index // 2 + 1}

        print("Predicted label:", max_correlation_index // 2)
        time.sleep(10)


while True: # Executar a função para processar os arquivos e plotar em tempo real
    simulation(directory)