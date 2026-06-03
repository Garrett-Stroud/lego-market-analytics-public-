from sold.build_sold_snapshot import build_sold_snapshot


def test_build_sold_snapshot(tmp_path, monkeypatch):
    def fake_loader(set_number, debug_file, use_saved):
        return """
        <html>
        <li class="s-card" data-listingid="123">
            <span aria-label="Sold Item">Sold May 28, 2024</span>

            <!-- TITLE -->
            <h3 class="s-item__title">LEGO COMPLETE</h3>

            <!-- CONDITION -->
            <span class="s-item__condition">Used</span>

            <!-- PRICE -->
            <span class="s-card__price">$10.00</span>

            <!-- SHIPPING -->
            <span class="s-item__shipping">$5.00</span>

            <!-- SELLER -->
            <div class="su-card-container__attributes__secondary">
                seller 100% positive (10)
            </div>
        </li>
        </html>
        """

    # IMPORTANT: patch the function reference used inside build_sold_snapshot
    monkeypatch.setattr("extraction.build_sold_snapshot.load_or_fetch_html", fake_loader)

    result = build_sold_snapshot(
        "1234",
        use_saved_html=True,   # IMPORTANT
        snapshot_dir=tmp_path
    )

    assert result["success"] is True
    assert len(result["listings"]) == 1
    assert result["listings"][0].item_id == "123"
