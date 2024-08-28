import requests
import json
import time

API_KEY = 'xxx'
LEAGUE_IDS = [
    39,   # Premier League
    140,  # La Liga
    78,   # Bundesliga
    135,  # Serie A
    61,   # Ligue 1
    2,    # UEFA Champions League
    3,    # UEFA Europa League
    64,   # Major League Soccer (MLS)
    88,   # Eredivisie
    94,   # Primeira Liga
    10,   # Brasileirão Serie A
    71,   # Argentine Primera División
    203,  # Russian Premier League
    253,  # Indian Super League
    82,   # Belgian Pro League
    72,   # Austrian Bundesliga
    307,  # Scottish Premiership
    13,   # Serie B (Italia)
    210,  # J1 League (Giappone)
    79,   # Bundesliga 2 (Germania)
    8,    # Eredivisie (Olanda)
    12,   # Ligue 2 (Francia)
    1,    # EFL Championship (Inghilterra)
    144,  # Super Lig (Turchia)
    76,   # Super League (Svizzera)
    108,  # Allsvenskan (Svezia)
    307,  # Premiership (Scozia)
    4,    # Serie A (Brasile)
    40,   # Brasileirao Serie A (Brasile)
    67,   # Championship (Inghilterra)
]  # Puoi aggiungere o rimuovere leghe da questa lista

SEASONS = [2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023]  # Ultimi 10 anni

headers = {
    'x-rapidapi-host': 'api-football-v1.p.rapidapi.com',
    'x-rapidapi-key': API_KEY
}

matches_data = []
for league_id in LEAGUE_IDS:
    for season in SEASONS:
        url = 'https://api-football-v1.p.rapidapi.com/v3/fixtures'
        params = {
            'league': league_id,
            'season': season
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()  # Lancia un'eccezione per errori HTTP

            fixtures = response.json().get('response')
            if not fixtures:
                print(f"Nessuna partita trovata per la lega {league_id} nella stagione {season}")
                continue

            for fixture in fixtures:
                match_info = {
                    "league_id": league_id,
                    "home_team": fixture['teams']['home']['name'],
                    "away_team": fixture['teams']['away']['name'],
                    "half_time_home_goals": fixture['score']['halftime']['home'],
                    "half_time_away_goals": fixture['score']['halftime']['away'],
                    "full_time_result": None,
                    "half_time_possession_home": None,
                    "half_time_possession_away": None,
                    "half_time_shots_home": None,
                    "half_time_shots_on_target_home": None,
                    "half_time_shots_away": None,
                    "half_time_shots_on_target_away": None
                }

                # Determinare il risultato finale
                full_time_home_goals = fixture['score']['fulltime']['home']
                full_time_away_goals = fixture['score']['fulltime']['away']
                if full_time_home_goals > full_time_away_goals:
                    match_info["full_time_result"] = "home_win"
                elif full_time_home_goals < full_time_away_goals:
                    match_info["full_time_result"] = "away_win"
                else:
                    match_info["full_time_result"] = "draw"

                # Dati delle statistiche del primo tempo (se disponibili)
                stats_url = 'https://api-football-v1.p.rapidapi.com/v3/fixtures/statistics'
                stats_params = {
                    'fixture': fixture['fixture']['id']
                }
                stats_response = requests.get(stats_url, headers=headers, params=stats_params)
                stats_response.raise_for_status()  # Controllo errori HTTP
                stats = stats_response.json().get('response')

                if stats:
                    for team_stats in stats:
                        if team_stats['team']['id'] == fixture['teams']['home']['id']:
                            match_info["half_time_possession_home"] = int(team_stats['statistics'][9]['value'].strip('%'))
                            match_info["half_time_shots_home"] = team_stats['statistics'][2]['value']
                            match_info["half_time_shots_on_target_home"] = team_stats['statistics'][3]['value']
                        elif team_stats['team']['id'] == fixture['teams']['away']['id']:
                            match_info["half_time_possession_away"] = int(team_stats['statistics'][9]['value'].strip('%'))
                            match_info["half_time_shots_away"] = team_stats['statistics'][2]['value']
                            match_info["half_time_shots_on_target_away"] = team_stats['statistics'][3]['value']

                matches_data.append(match_info)
                # Evitare di superare il limite di richieste all'API
                time.sleep(2)

            # Evitare di superare il limite di richieste all'API
            time.sleep(5)

        except requests.exceptions.HTTPError as http_err:
            print(f"Errore HTTP per la lega {league_id} nella stagione {season}: {http_err}")
        except Exception as err:
            print(f"Errore imprevisto per la lega {league_id} nella stagione {season}: {err}")

# Scrittura del file JSON solo se ci sono dati
if matches_data:
    with open('matches.json', 'w') as outfile:
        json.dump(matches_data, outfile, indent=4)
    print(f"File 'matches.json' creato con successo con {len(matches_data)} partite!")
else:
    print("Nessun dato trovato, il file 'matches.json' non è stato creato.")
