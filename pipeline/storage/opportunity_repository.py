import json
from models.opportunity import Opportunity
from pipeline.storage.db import get_connection


class OpportunityRepository:

    # -----------------------------
    # Save
    # -----------------------------
    def save(self, run_id: str, opp: Opportunity):
        with get_connection() as conn:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO opportunities (
                    run_id, product_key,
                    buy_source, buy_price, buy_url,
                    sell_source, sell_price, sell_url,
                    profit, roi, score, score_details
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                run_id,
                opp.product_key,
                opp.buy_source,
                opp.buy_price,
                opp.buy_url,
                opp.sell_source,
                opp.sell_price,
                opp.sell_url,
                opp.profit,
                opp.roi,
                opp.score,
                json.dumps(opp.score_details),
            ))

            conn.commit()

    # -----------------------------
    # Get latest run ID
    # -----------------------------
    def get_latest_run_id(self) -> str | None:
        with get_connection() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT run_id
                FROM opportunities
                ORDER BY created_at DESC
                LIMIT 1
            """)

            row = cur.fetchone()
            return row["run_id"] if row else None

    # -----------------------------
    # Row mapper
    # -----------------------------
    def _map_row(self, r):
        return {
            "product_key": r["product_key"],
            "buy_price": r["buy_price"],
            "sell_price": r["sell_price"],
            "profit": r["profit"],
            "roi": r["roi"],
            "score": r["score"],
            "buy_url": r["buy_url"],
            "score_details": json.loads(r["score_details"]),
        }

    # -----------------------------
    # Get by run
    # -----------------------------
    def get_by_run(self, run_id: str):
        with get_connection() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT *
                FROM opportunities
                WHERE run_id = ?
                ORDER BY score DESC
            """, (run_id,))

            return [self._map_row(r) for r in cur.fetchall()]

    # -----------------------------
    # Get by set number
    # -----------------------------
    def get_by_set_number(self, set_number: str):
        with get_connection() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT *
                FROM opportunities
                WHERE product_key = ?
                ORDER BY created_at DESC
            """, (set_number,))

            return [self._map_row(r) for r in cur.fetchall()]