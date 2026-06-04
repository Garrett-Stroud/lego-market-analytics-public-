from flask import Flask, render_template, jsonify, request
from pipeline.storage.opportunity_storage import (
    list_opportunities,
    record_event,
    get_history,
)
from pipeline.db import get_conn

app = Flask(__name__)

@app.route("/")
def index():
    rows = list_opportunities()
    opportunities = [
        {
            "id": r[0],
            "product_key": r[1],
            "title": r[2],  # now product_title
            "buy_source": r[3],
            "buy_price": r[4],
            "sell_source": r[5],
            "sell_price": r[6],
            "profit": r[7],
            "roi": r[8],
            "score": r[9],
            "score_details": r[10],
            "buy_url": r[11],
            "sell_url": r[12],
            "created_at": r[13],
        }
        for r in rows
    ]
    return render_template("index.html", opportunities=opportunities)


@app.route("/buy/<int:opp_id>", methods=["POST"])
def buy(opp_id):
    record_event(opp_id, "BOUGHT")
    _delete_opportunity(opp_id)
    return jsonify({"success": True})


@app.route("/delete/<int:opp_id>", methods=["POST"])
def delete(opp_id):
    record_event(opp_id, "DELETED")
    _delete_opportunity(opp_id)
    return jsonify({"success": True})


@app.route("/history/<int:opp_id>")
def history(opp_id):
    rows = get_history(opp_id)
    return jsonify([
        {"event": r[0], "timestamp": r[1]}
        for r in rows
    ])


def _delete_opportunity(opp_id: int) -> None:
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM opportunities WHERE id = ?", (opp_id,))
    conn.commit()
    conn.close()
