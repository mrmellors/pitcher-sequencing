import duckdb
import pandas as pd
from pathlib import Path

# reads in the statcast data from the database for 2025 season

db_path = Path("~/repos/statcast-database/statcast.duckdb").expanduser()

conn = duckdb.connect(str(db_path))
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
        events,
        woba_value,
        woba_denom,
        estimated_woba_using_speedangle
    FROM statcast
    WHERE game_date >= '2025-03-27'
      AND game_date <= '2025-11-30'
    ORDER BY game_pk, at_bat_number, pitch_number
""").df()

# designates the pitching team based on the top or the bottom half of the inning
df["pitching_team"] = df["home_team"].where(
    df["inning_topbot"] == "Top",
    df["away_team"]
)

# then groups by the gameID(pk), game_date, pitching_team, pitcherID, and player_name
# it then aggregates globally the pitchers first AB number in the game, last, and the nunmber of pitches
appearances = (
    df.groupby(
        ["game_pk", "game_date", "pitching_team", "pitcher", "player_name"],
        as_index=False
    )
    .agg(
        first_ab=("at_bat_number", "min"),
        last_ab=("at_bat_number", "max"),
        pitches=("pitch_number", "size")
    )
)

appearances.head()


# just sorts the df by the player who entered the game first so that we can later add previous pitcher
appearances = appearances.sort_values(
    ["game_pk", "pitching_team", "first_ab"]
)

# groups by game and pitching team and then shifts the previous pitcher value down 1 as the previous pitcher
appearances["previous_pitcher"] = (
    appearances
    .groupby(["game_pk", "pitching_team"])["pitcher"]
    .shift(1)
)

appearances["previous_pitcher_name"] = (
    appearances
    .groupby(["game_pk", "pitching_team"])["player_name"]
    .shift(1)
)


# groups by game, pitching_team, and pitcher and then gets unique AB #'s 
# to determine the amount of batters a pitcher has faced resulted in a final outcome
# filtered out events that were truncated_pa like caught stealing, pick off
completed_pa = df[
    df["events"].notna() &
    (df["events"] != "truncated_pa")
].copy()

pa_counts = (
    completed_pa
    .groupby(["game_pk", "pitching_team", "pitcher"])
    .size()
    .reset_index(name="completed_pa")
)

appearances = appearances.merge(
    pa_counts,
    on=["game_pk", "pitching_team", "pitcher"],
    how="left"
)

appearances["completed_pa"] = appearances["completed_pa"].fillna(0).astype(int)


# xwoba_pa is just the plate appearances where there is a valid xwoba
xwoba_pa = completed_pa[
    completed_pa["estimated_woba_using_speedangle"].notna()
].copy()

xwoba_pa["pa_xwoba"] = xwoba_pa[
    "estimated_woba_using_speedangle"
]


# appearance_xwoba is then just the sum(xwoba for every PA) / plate appearances where there is a valid xwoba
# sum(pa_xwoba)/xwoba_pa
appearance_xwoba = (
    xwoba_pa
    .groupby(["game_pk", "pitching_team", "pitcher"])
    .agg(
        appearance_xwoba=("pa_xwoba", "mean"),
        xwoba_pa=("pa_xwoba", "size")
    )
    .reset_index()
)

# adding the mean xwoba from that appearance to the df
appearances = appearances.merge(
    appearance_xwoba,
    on=["game_pk", "pitching_team", "pitcher"],
    how="left"
)

appearances.head()