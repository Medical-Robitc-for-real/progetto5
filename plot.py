import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# 1. Caricamento dei dati
# Legge il file, specificando il delimitatore come tab ('\t')
try:
    data = pd.read_csv('work_space_1.txt', delimiter='\t')
except FileNotFoundError:
    print("Errore: Il file 'work_space_minus_50.txt' non è stato trovato.")
    # Puoi uscire o usare un DataFrame di esempio qui, a seconda di come vuoi gestire l'errore
    exit()

# 2. Assegnazione delle variabili (facoltativa ma utile per chiarezza)
# Si accede direttamente alle colonne del DataFrame
ins1 = data['Ins1']
rot1 = data['Rot1']
ins2 = data['Ins2']
rot2 = data['Rot2']
ins3 = data['Ins3'] # Colonna usata per colorare lo scatter plot
rot3 = data['Rot3']
X = data['X']
Y = data['Y']
Z = data['Z']

# 3. Creazione e configurazione del grafico 3D
# Crea una nuova figura e un sottoplot 3D
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d') # '111' è la sintassi per una griglia 1x1, primo subplot

# Scatter plot 3D
# Il parametro 'c' definisce i colori, 'cmap' la mappa colori (jet), 's' la dimensione dei punti
scatter = ax.scatter(X, Y, Z, c=ins3, cmap='jet', s=20, marker='o')

# Etichette e Titolo
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('3D Workspace del tubo 3')

# Limiti degli assi
ax.set_xlim([-50, 50])
ax.set_ylim([-50, 50])
ax.set_zlim([0, 200])

# Griglia
ax.grid(True)

# Colorbar (barra dei colori)
# Si aggiunge la colorbar, specificando lo scatter object a cui si riferisce
fig.colorbar(scatter, ax=ax)

# Mostra il grafico
plt.show()
