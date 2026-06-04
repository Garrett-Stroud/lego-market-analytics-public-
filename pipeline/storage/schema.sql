-- ============================================================
-- RUNS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- JOINED SNAPSHOTS TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS joined_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,

    set_number TEXT,
    rb_name TEXT,
    rb_theme TEXT,
    rb_year INTEGER,
    rb_num_parts INTEGER,

    active_lowest REAL,
    active_median REAL,
    active_count INTEGER,

    sold_median REAL,
    sold_min REAL,
    sold_max REAL,
    sold_count INTEGER,

    sold_count_30d INTEGER,
    sold_count_90d INTEGER,
    volatility REAL,
    trend REAL,


    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (run_id) REFERENCES runs(id)
);

-- ============================================================
-- OPPORTUNITIES TABLE
-- ============================================================
CREATE TABLE IF NOT EXISTS opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    product_key TEXT NOT NULL,
    product_title TEXT,
    image_url TEXT,


    buy_source TEXT,
    buy_price REAL,
    buy_url TEXT,

    sell_source TEXT,
    sell_price REAL,
    sell_url TEXT,

    profit REAL,
    roi REAL,
    score REAL,
    score_details TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (run_id) REFERENCES runs(id)
);
