import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.utils import to_categorical
import json
import joblib

# Caricamento dei dati dal file JSON
with open('matches.json', 'r') as file:
    data = json.load(file)

# Preparazione delle feature e del target
X = []
y = []

for match in data:
    home_goal_diff = match['half_time_home_goals'] - match['half_time_away_goals']
    possession_diff = match['half_time_possession_home'] - match['half_time_possession_away']
    shots_on_target_diff = match['half_time_shots_on_target_home'] - match['half_time_shots_on_target_away']

    # Feature: differenza gol, differenza possesso palla, differenza tiri in porta
    X.append([home_goal_diff, possession_diff, shots_on_target_diff])

    # Target: risultato finale
    y.append(match['full_time_result'])

X = np.array(X)

# Conversione del target in valori numerici
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(y)
y = to_categorical(y)  # Conversione in categorie per Keras (es. [1, 0, 0] per "home_win")

# Divisione in training e testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creazione del modello
model = Sequential()
model.add(Dense(64, input_dim=3, activation='relu'))  # Input: 3 feature
model.add(Dense(32, activation='relu'))
model.add(Dense(3, activation='softmax'))  # Output: 3 classi (home_win, away_win, draw)

# Compilazione del modello
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Addestramento del modello
model.fit(X_train, y_train, epochs=50, batch_size=10, validation_data=(X_test, y_test))

# Valutazione del modello
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Accuracy: {accuracy * 100:.2f}%')

# Salvataggio del modello
model.save('soccer_prediction_model.h5')

# Salvataggio del label encoder
joblib.dump(label_encoder, 'label_encoder.pkl')

print("Modello e label encoder salvati correttamente.")
