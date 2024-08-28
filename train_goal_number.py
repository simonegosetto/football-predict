import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
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

    # Target: numero totale di gol nel secondo tempo
    full_time_home_goals = match['half_time_home_goals'] + match.get('full_time_home_goals', 0)
    full_time_away_goals = match['half_time_away_goals'] + match.get('full_time_away_goals', 0)
    second_half_goals = (full_time_home_goals - match['half_time_home_goals']) + \
                        (full_time_away_goals - match['half_time_away_goals'])
    y.append(second_half_goals)

X = np.array(X)
y = np.array(y)

# Divisione in training e testing set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Creazione del modello
model = Sequential()
model.add(Dense(64, input_dim=3, activation='relu'))  # Input: 3 feature
model.add(Dense(32, activation='relu'))
model.add(Dense(1, activation='linear'))  # Output: numero di gol (regressione)

# Compilazione del modello
model.compile(loss='mean_squared_error', optimizer='adam')

# Addestramento del modello
model.fit(X_train, y_train, epochs=50, batch_size=10, validation_data=(X_test, y_test))

# Valutazione del modello
loss = model.evaluate(X_test, y_test)
print(f'Loss (MSE): {loss}')

# Salvataggio del modello
model.save('goal_prediction_model.h5')

print("Modello salvato correttamente.")
