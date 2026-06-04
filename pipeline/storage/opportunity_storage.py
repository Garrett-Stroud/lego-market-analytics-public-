import json
from datetime import datetime, UTC
from typing import List

from pipeline.storage.db import get_connection
from models.opportunity import Opportunity


class OpportunityStorage:
    """
    High-level storage interface for saving and retrieving opportunities
    and tracking user events.
    """

    # ---------------------------------------------------------
    # Store opportunities
    # ---------------------------------------------------------
    def store_opportunities(self, opportunities: List[Opportunity]) -> None:
        with get_connection() as conn:
            cur = conn.cursor()

            rows = [
                (
                    o.product_key,
                    getattr(o, "product_title", None),

                    o.buy_source,
                    o.buy_price,
                    o.sell_source,
                    o.sell_price,
                    o.profit,
                    o.roi,
                    o.score,
                    json.dumps(o.score_details) if o.score_details else None,
                    o.buy_url,
                    o.sell_url,
                    datetime.now(UTC).isoformat()
                )
                for o in opportunities
            ]

            cur.executemany("""
                INSERT INTO opportunities (
                    product_key, product_title, buy_source, buy_price,
                    sell_source, sell_price, profit, roi, score,
                    score_details, buy_url, sell_url, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, rows)

            conn.commit()

    # ---------------------------------------------------------
    # List opportunities
    # ---------------------------------------------------------
    def list_opportunities(self, limit: int = 200):
        with get_connection() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT id, product_key, product_title, buy_source, buy_price,
                       sell_source, sell_price, profit, roi, score,
                       score_details, buy_url, sell_url, created_at
                FROM opportunities
                ORDER BY score DESC, profit DESC
                LIMIT ?
            """, (limit,))

            return cur.fetchall()

    # ---------------------------------------------------------
    # Record user events
    # ---------------------------------------------------------
    def record_event(self, opportunity_id: int, event_type: str) -> None:
        with get_connection() as conn:
            cur = conn.cursor()

            cur.execute("""
                INSERT INTO opportunity_events (opportunity_id, event_type, created_at)
                VALUES (?, ?, ?)
            """, (opportunity_id, event_type, datetime.now(UTC).isoformat()))

            conn.commit()

    # ---------------------------------------------------------
    # Get event history
    # ---------------------------------------------------------
    def get_history(self, opportunity_id: int):
        with get_connection() as conn:
            cur = conn.cursor()

            cur.execute("""
                SELECT event_type, created_at
                FROM opportunity_events
                WHERE opportunity_id = ?
                ORDER BY created_at DESC
            """, (opportunity_id,))

            return cur.fetchall()