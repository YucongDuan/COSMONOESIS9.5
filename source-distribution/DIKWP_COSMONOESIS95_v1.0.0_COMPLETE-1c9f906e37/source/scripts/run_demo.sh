#!/usr/bin/env sh
set -eu
python run.py doctor
python run.py demo --out outputs/cosmonoesis_demo
python run.py verify outputs/cosmonoesis_demo
