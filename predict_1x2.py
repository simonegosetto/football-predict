import numpy as np
from tensorflow.keras.models import load_model
import joblib

# Caricamento del modello e del label encoder
model = load_model('soccer_prediction_model.h5')
label_encoder = joblib.load('label_encoder.pkl')

# Dati di esempio per una partita live
goal_diff = 1  # Differenza gol
possession_diff = 10  # Differenza possesso palla
shots_on_target_diff = 2  # Differenza tiri in porta

# Prepara i dati per la predizione
live_data = np.array([[goal_diff, possession_diff, shots_on_target_diff]])

# Effettua la predizione
prediction = model.predict(live_data)
predicted_class = np.argmax(prediction, axis=1)

# Conversione della predizione nella classe originale (es. 'home_win')
result = label_encoder.inverse_transform(predicted_class)
print(f'Risultato previsto: {result[0]}')
