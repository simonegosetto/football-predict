import numpy as np
from tensorflow.keras.models import load_model

# Caricamento del modello
model = load_model('goal_prediction_model.h5')

# Dati di esempio per una partita live (differenza gol, possesso palla, tiri in porta nel primo tempo)
goal_diff = 1  # Differenza gol
possession_diff = 1  # Differenza possesso palla
shots_on_target_diff = -1  # Differenza tiri in porta

# Prepara i dati per la predizione
live_data = np.array([[goal_diff, possession_diff, shots_on_target_diff]])

# Effettua la predizione
predicted_goals = model.predict(live_data)
predicted_goals = max(0, predicted_goals[0][0])  # Imposta il minimo a 0
print(f'Numero di gol previsto nel secondo tempo: {predicted_goals:.2f}')

