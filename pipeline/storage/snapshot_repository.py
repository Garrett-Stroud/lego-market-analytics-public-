from pipeline.storage.db import get_connection


class SnapshotRepository:

    # -----------------------------
    # Save
    # -----------------------------
    def save(self, run_id: str, snapshot):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO joined_snapshots (
                run_id, set_number, rb_name, rb_theme, rb_year, rb_num_parts,
                active_lowest, active_median, active_count,
                sold_median, sold_min, sold_max, sold_count,
                sold_count_30d, sold_count_90d, volatility, trend
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            run_id,
            snapshot.set_number,
            snapshot.rb_name,
            snapshot.rb_theme,
            snapshot.rb_year,
            snapshot.rb_num_parts,
            snapshot.active_lowest,
            snapshot.active_median,
            snapshot.active_count,
            snapshot.sold_median,
            snapshot.sold_min,
            snapshot.sold_max,
            snapshot.sold_count,
            snapshot.sold_count_30d,
            snapshot.sold_count_90d,
            snapshot.volatility,
            snapshot.trend,
        ))

        conn.commit()
        conn.close()

    # -----------------------------
    # Get all runs
    # -----------------------------
    def get_all_runs(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT 
                js.run_id,
                COUNT(*) AS snapshot_count,
                MIN(js.created_at) AS created_at,
                (
                    SELECT COUNT(*)
                    FROM opportunities o
                    WHERE o.run_id = js.run_id
                ) AS opportunity_count
            FROM joined_snapshots js
            GROUP BY js.run_id
            ORDER BY created_at DESC
        """)

        rows = cur.fetchall()
        conn.close()

        return [
            {
                "run_id": r["run_id"],
                "snapshot_count": r["snapshot_count"],
                "opportunity_count": r["opportunity_count"] or 0,
                "created_at": r["created_at"],
            }
            for r in rows
        ]

    # -----------------------------
    # Get snapshots for a run
    # -----------------------------
    def get_by_run(self, run_id: str):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM joined_snapshots
            WHERE run_id = ?
            ORDER BY set_number
        """, (run_id,))

        rows = cur.fetchall()
        conn.close()

        return [dict(r) for r in rows]

    # -----------------------------
    # Get snapshots for a set
    # -----------------------------
    def get_by_set_number(self, set_number: str):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT *
            FROM joined_snapshots
            WHERE set_number = ?
            ORDER BY created_at DESC
        """, (set_number,))

        rows = cur.fetchall()
        conn.close()

        return [dict(r) for r in rows]
