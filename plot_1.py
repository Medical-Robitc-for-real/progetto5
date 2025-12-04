import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Lista dei file e titoli corrispondenti
files = [
    ('work_space_nominal.txt', 'Workspace nominale'),
    ('workspace_minus20.txt', 'Workspace con -20% parameteri nominali'),
    ('workspace_plus20.txt', 'Workspace con +20% parametri nominali')
]

# Crea figura con 3 subplot 3D affiancati
fig = plt.figure(figsize=(18, 6))

for i, (filename, title) in enumerate(files):
    try:
        data = pd.read_csv(filename, delimiter='\t')
    except FileNotFoundError:
        print(f"Errore: Il file '{filename}' non è stato trovato.")
        continue

    # Estrazione colonne
    X = data['X']
    Y = data['Y']
    Z = data['Z']
    # Usiamo Ins3 per colorare i punti
    c = data['Ins3']

    # Crea il subplot 3D
    ax = fig.add_subplot(1, 3, i+1, projection='3d')
    scatter = ax.scatter(X, Y, Z, c=c, cmap='jet', s=20, marker='o')

    # Etichette e titolo
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)

    # Limiti degli assi (personalizzabili)
    ax.set_xlim([-50, 50])
    ax.set_ylim([-50, 50])
    ax.set_zlim([0, 200])
    ax.grid(True)

    # Colorbar per ogni subplot
    fig.colorbar(scatter, ax=ax, shrink=0.5, aspect=10)

plt.tight_layout()
plt.show()

