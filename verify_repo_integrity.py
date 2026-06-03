"""
verify_repo_integrity.py

Runs a full post-refactor health check on the LEGO Market Analytics repo.
"""

import importlib
import json
import subprocess
import sys
from pathlib import Path


def check_import(path: str):
    try:
        importlib.import_module(path)
        print(f"[OK] Import: {path}")
        return True
    except Exception as e:
        print(f"[FAIL] Import: {path}")
        print(f"       {e}")
        return False


def run_python_snippet(code: str, label: str):
    try:
        subprocess.check_output([sys.executable, "-c", code])
        print(f"[OK] {label}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[FAIL] {label}")
        print(e.output.decode())
        return False


def check_pipeline_demo():
    print("\n=== Running pipeline_demo_run.py ===")
    try:
        out = subprocess.check_output(
            [sys.executable, "pipeline/pipeline_demo_run.py"],
            stderr=subprocess.STDOUT,
        ).decode()
        print("[OK] pipeline_demo_run.py executed")
        print(out)
        return True
    except subprocess.CalledProcessError as e:
        print("[FAIL] pipeline_demo_run.py")
        print(e.output.decode())
        return False


def check_fastapi():
    print("\n=== Checking FastAPI health (if running) ===")
    import urllib.request

    try:
        with urllib.request.urlopen("http://localhost:8000/docs") as r:
            if r.status == 200:
                print("[OK] FastAPI server is running at http://localhost:8000")
                return True
    except Exception:
        print("[WARN] FastAPI not running (this is fine unless you're testing the dashboard API)")
        return False


def main():
    print("\n=== LEGO Market Analytics — Repo Integrity Check ===\n")

    # -----------------------------
    # 1. Import checks
    # -----------------------------
    print("=== Import Checks ===")

    imports = [
        # Canonicalization
        "pipeline.canonicalization.browse_adapter",
        "pipeline.canonicalization.canonicalize_sold_snapshot",
        "pipeline.canonicalization.completeness",
        "pipeline.canonicalization.condition",
        "pipeline.canonicalization.date_utils",
        "pipeline.canonicalization.dates",
        "pipeline.canonicalization.grouping",
        "pipeline.canonicalization.prices",
        "pipeline.canonicalization.seller",
        "pipeline.canonicalization.set_number_extractor",
        "pipeline.canonicalization.sold_adapter",
        "pipeline.canonicalization.sold_adapter_validator",
        "pipeline.canonicalization.sold_batch_validator",
        "pipeline.canonicalization.sold_validator",

        # Enrichment
        "pipeline.enrichment.rebrickable_client",
        "pipeline.enrichment.rebrickable_enricher",
        "pipeline.enrichment.rebrickable_index",
        "pipeline.enrichment.theme_helpers",

        # Features
        "pipeline.features.attribute_extractor",
        "pipeline.features.feature_builder",
        "pipeline.features.finalize_matrix",
        "pipeline.features.sold_feature_builder",

        # Ingestion
        "pipeline.ingestion.browse_client_raw",
        "pipeline.ingestion.ebay_auth",
        "pipeline.ingestion.ebay_sold_client",
        "pipeline.ingestion.finding_client_raw",

        # Join
        "pipeline.join.active_sold_joiner",

        # Scoring
        "pipeline.scoring.score_snapshot",
        "pipeline.scoring.score_opprtunity",

        # Storage
        "pipeline.storage.db",
        "pipeline.storage.init_db",
        "pipeline.storage.opportunity_repository",
        "pipeline.storage.opportunity_storage",
        "pipeline.storage.snapshot_repository",
        "pipeline.storage.storage",

        # Config
        "pipeline.config.load_config",
    ]

    for module in imports:
        check_import(module)

    # -----------------------------
    # 2. Pipeline demo test
    # -----------------------------
    check_pipeline_demo()

    # -----------------------------
    # 3. FastAPI health check
    # -----------------------------
    check_fastapi()

    print("\n=== Integrity Check Complete ===\n")


if __name__ == "__main__":
    main()
