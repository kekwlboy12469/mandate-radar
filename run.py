#!/usr/bin/env python3
"""
Mandate Radar Root Launcher
Runs the unified FastAPI backend and embedded React frontend.
"""
import os
import sys
import uvicorn

if __name__ == "__main__":
    backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend"))
    sys.path.insert(0, backend_dir)
    os.chdir(backend_dir)
    print("=" * 65)
    print("  ⚡ MANDATE RADAR: THE AUTO DEBITS NOBODY CAN FIND")
    print("  Track: Neo4j (Best Use of Neo4j) | Theme: Fintech")
    print("  Serving Web UI & API at: http://127.0.0.1:8000")
    print("=" * 65)
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=False)
