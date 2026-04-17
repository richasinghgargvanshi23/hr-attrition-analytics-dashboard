"""
run_pipeline.py
────────────────────────────────────────────────────────────────────────────
HR Attrition Analytics  –  Master Pipeline Runner
────────────────────────────────────────────────────────────────────────────
Runs all project steps in sequence:
  Step 0  → Generate raw dataset   (scripts/generate_dataset.py)
  Step 1  → Clean & engineer data   (scripts/01_data_cleaning.py)
  Step 2  → Exploratory analysis    (scripts/02_exploratory_analysis.py)
  Step 3  → SQL analysis            (scripts/03_sql_analysis.py)
  Step 4  → Predictive modeling     (scripts/04_attrition_modeling.py)
  Step 5  → Dashboard preview       (scripts/05_dashboard_preview.py)

Usage:
    python run_pipeline.py
"""

import subprocess
import sys
import os
import time

BASE    = os.path.dirname(os.path.abspath(__file__))
PYTHON  = sys.executable

STEPS = [
    ("Generate Dataset",        os.path.join(BASE, "scripts", "generate_dataset.py")),
    ("Data Cleaning",           os.path.join(BASE, "scripts", "01_data_cleaning.py")),
    ("Exploratory Analysis",    os.path.join(BASE, "scripts", "02_exploratory_analysis.py")),
    ("SQL Analysis",            os.path.join(BASE, "scripts", "03_sql_analysis.py")),
    ("Predictive Modeling",     os.path.join(BASE, "scripts", "04_attrition_modeling.py")),
    ("Dashboard Preview",       os.path.join(BASE, "scripts", "05_dashboard_preview.py")),
]

def run_step(name, script_path):
    print(f"\n{'='*60}")
    print(f"  STEP: {name}")
    print(f"{'='*60}")
    start = time.time()
    result = subprocess.run([PYTHON, script_path], capture_output=False, text=True)
    elapsed = time.time() - start
    if result.returncode != 0:
        print(f"\n❌  FAILED: {name}  (exit code {result.returncode})")
        sys.exit(result.returncode)
    else:
        print(f"\n✅  Completed in {elapsed:.1f}s")

if __name__ == "__main__":
    print("=" * 60)
    print("   HR ATTRITION ANALYTICS  –  FULL PIPELINE")
    print("=" * 60)
    total_start = time.time()

    for step_name, script in STEPS:
        run_step(step_name, script)

    total_elapsed = time.time() - total_start
    print(f"\n{'='*60}")
    print(f"  ALL STEPS COMPLETE  ({total_elapsed:.0f}s total)")
    print(f"{'='*60}")
    print("\n📁  Outputs:")
    out_dir = os.path.join(BASE, "outputs")
    for f in sorted(os.listdir(out_dir)):
        fpath = os.path.join(out_dir, f)
        size  = os.path.getsize(fpath) // 1024
        print(f"   {f:<45} {size:>5} KB")
    print(f"\n  📊 Power BI file: dashboard/powerbi_setup_guide.md")
    print(f"  📄 Documentation:  docs/project_report.md")
