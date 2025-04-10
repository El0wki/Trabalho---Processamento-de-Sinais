"""
Exemplo de uso da classe serial_lib.py com gráfico em tempo real
Desenvolvido por: Adalberto Oliveira
Fainor - Curso de Engenharia de Computação
Processamento Digital de Sinais
Outubro de 2024
"""

import time
import matplotlib.pyplot as plt
import numpy as np
from serial_lib import SerialCommunication
from processamento_lib import Processamento
from collections import deque

# Definições da porta serial
port = "COM6"
baud_rate = 9600

serial = SerialCommunication(port=port, baud_rate=baud_rate, data_length=1, health_test=True, timeout=0.1)
serial.start()
pds = Processamento(vin=12, tensao_base=5)

# Configuração do gráfico
plt.ion()  # Ativa o modo interativo do Matplotlib
fig, ax = plt.subplots()
x_data = deque(maxlen=100)  # Janela deslizante de 100 pontos
y_data = deque(maxlen=100)  
line, = ax.plot([], [], 'r-')  

tick = time.time()
tempo = 0  # Contador de tempo

while True:
    if (time.time() - tick) > 0.001:
        tick = time.time()

        # Lendo a porta serial
        serial_data = serial.get_data()

        if serial_data:
            valor = serial_data[0]
            tensao = pds.tensao(valor)

            # Atualizando os dados do gráfico
            tempo += 1  # Simula o eixo X
            x_data.append(tempo)
            y_data.append(tensao)

            # Atualizando o gráfico
            line.set_xdata(x_data)
            line.set_ydata(y_data)
            ax.relim()
            ax.autoscale_view()
            plt.draw()
            plt.pause(0.0001)

            print(f"Amostra: {round(pds.amostra,2)} Tensao: {round(tensao,2)}", end="\r")
