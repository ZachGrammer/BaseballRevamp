DROP TABLE IF EXISTS analytics.player_season_summary;

CREATE TABLE analytics.player_season_summary (
    season INT NOT NULL,
    batter BIGINT NOT NULL,

    pa_count INT,
    woba_denom_value INT,

    expected_numerator DOUBLE PRECISION,
    actual_numerator DOUBLE PRECISION,

    xwoba DOUBLE PRECISION,
    woba DOUBLE PRECISION,
    woba_minus_xwoba DOUBLE PRECISION,
    xwoba_minus_woba DOUBLE PRECISION,

    bb INT,
    ibb INT,
    hbp_event INT,
    sf INT,
    ab INT,
    hit INT,
    single INT,
    double INT,
    triple INT,
    home_run INT,

    PRIMARY KEY (season, batter)
);