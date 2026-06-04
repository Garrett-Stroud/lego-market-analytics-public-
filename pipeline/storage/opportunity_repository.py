import json

from pipeline.storage.db import get_connection



class OpportunityRepository:

    # -----------------------------
    # Create a new run
    # -----------------------------
    def create_run(self) -> int:
        with get_connection() as conn:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO runs (created_at)
                VALUES (CURRENT_TIMESTAMP)
            """)

            conn.commit()
            return cur.lastrowid

    # -----------------------------
    # Save
    # -----------------------------
    def save(self, run_id: str, opp):

        # If it's a dict, use it directly
        if isinstance(opp, dict):
            data = opp
        else:
            data = opp.model_dump()

        with get_connection() as conn:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO opportunities (
                    run_id, product_key,
                    buy_source, buy_price, buy_url,
                    sell_source, sell_price, sell_url,
                    profit, roi, score, score_details,
                    product_title, image_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                run_id,
                data.get("product_key"),
                data.get("buy_source"),
                data.get("buy_price"),
                data.get("buy_url"),
                data.get("sell_source"),
                data.get("sell_price"),
                data.get("sell_url"),
                data.get("profit"),
                data.get("roi"),
                data.get("score"),
                json.dumps(data.get("score_details") or {}),
                data.get("product_title"),
                data.get("image_url"),
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
            "id": r["id"],
            "product_key": r["product_key"],

            # Correct fields
            "title": r["product_title"],
            "image_url": r["image_url"],

            "buy_price": r["buy_price"],
            "sell_price": r["sell_price"],
            "profit": r["profit"],
            "roi": r["roi"],
            "score": r["score"],
            "buy_url": r["buy_url"],
            "sell_url": r["sell_url"],
            "score_details": json.loads(r["score_details"]) if r["score_details"] else {},
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
