#!/bin/bash

alembic upgrade head

uvicorn wedding.app:app --host 0.0.0.0 --port 8000
