from pathlib import Path
import json


# ------------------------------------------------------------
# Paths
# ------------------------------------------------------------


ROOT = Path(__file__).resolve().parents[1]
EXAMPLES_DIR = ROOT / "data" / "examples"


# ------------------------------------------------------------
# Helpers
# ------------------------------------------------------------
def load_json(filename: str):
    with open(EXAMPLES_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


# ------------------------------------------------------------
# STEP 1: Load raw listing
# ------------------------------------------------------------
def load_raw():
    return load_json("01_raw_active_listing.json")


# ------------------------------------------------------------
# STEP 2: Canonicalization (demo version)
# ------------------------------------------------------------
def canonicalize(raw):
    return load_json("02_canonical_item.json")


# ------------------------------------------------------------
# STEP 3: Grouping by set number
# ------------------------------------------------------------
def group_by_set(canonical_item):
    set_number = canonical_item["set_number"]

    return {
        set_number: [canonical_item]
    }


# ------------------------------------------------------------
# STEP 4: Load sold feature set
# ------------------------------------------------------------
def load_sold_features():
    return load_json("04_sold_feature_set.json")


# ------------------------------------------------------------
# STEP 5: Build snapshot (active + sold join)
# ------------------------------------------------------------
def build_snapshot(set_number, grouped_active, sold_features):
    return load_json("05_snapshot.json")


# ------------------------------------------------------------
# STEP 6: Score opportunity
# ------------------------------------------------------------
def score(snapshot):
    opp = load_json("06_opportunity.json")
    return opp


# ------------------------------------------------------------
# MAIN DEMO PIPELINE
# ------------------------------------------------------------
def run_demo_pipeline():
    print("\n=== LEGO Pipeline Demo Run ===\n")

    # 1. Raw ingestion
    raw = load_raw()
    print("[1] Raw listing loaded")

    # 2. Canonicalization
    canonical = canonicalize(raw)
    print("[2] Canonical item created")

    # 3. Grouping
    grouped = group_by_set(canonical)
    set_number = list(grouped.keys())[0]
    print(f"[3] Grouped by set: {set_number}")

    # 4. Sold features
    sold_features = load_sold_features()
    print("[4] Sold market features loaded")

    # 5. Snapshot join
    snapshot = build_snapshot(set_number, grouped, sold_features)
    print("[5] Snapshot created (active + sold joined)")

    # 6. Scoring
    opportunity = score(snapshot)
    print("[6] Opportunity scored")

    # ------------------------------------------------------------
    # Output
    # ------------------------------------------------------------
    print("\n=== FINAL OUTPUT ===\n")
    print(json.dumps(opportunity, indent=2))


# ------------------------------------------------------------
# Entry point
# ------------------------------------------------------------
if __name__ == "__main__":
    run_demo_pipeline()