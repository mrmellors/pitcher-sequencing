import duckdb
import pandas as pd

conn = duckdb.connect("statcast.duckdb")

df = conn.execute("""
    SELECT
        game_pk,
        game_date,
        inning,
        inning_topbot,
        at_bat_number,
        pitch_number,
        pitcher,
        player_name,
        home_team,
        away_team,
        estimated_woba_using_speedangle
    FROM statcast
    WHERE game_date >= '2025-03-27'
      AND game_date <= '2025-11-30'
    ORDER BY game_pk, at_bat_number, pitch_number
""").df()

df