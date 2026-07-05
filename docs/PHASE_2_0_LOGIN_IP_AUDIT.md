# Phase 2.0 Login IP Audit for Future Streamlit Analytics

This phase adds a login audit trail so every login attempt can be analyzed later in Streamlit.

## What is saved

Each login attempt writes one row in `school_loginactivity`:

- `user`
- `username_entered`
- `ip_address`
- `forwarded_for`
- `user_agent`
- `path`
- `method`
- `is_successful`
- `failure_reason`
- `session_key`
- `role_snapshot`
- `created_at`

Future geo enrichment fields are also ready:

- `city`
- `region`
- `country_code`
- `country_name`
- `latitude`
- `longitude`
- `timezone`

## Important note about location

Local development usually records `127.0.0.1` or `::1`, because the browser and Django server are running on the same computer.

Real public IP/location will become useful when the app is deployed online behind a proper server/proxy. At that point we can enrich the saved IPs using an IP-to-location database or API and then visualize them in Streamlit.

## Django Admin

Open Django Admin and look for:

```text
Login activities
```

You can filter by success/failure, date, city/country once enriched, and search by username/IP/user-agent.

## Streamlit-ready example query

For SQLite local development:

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect('db.sqlite3')
df = pd.read_sql_query('''
    SELECT created_at, username_entered, ip_address, is_successful,
           failure_reason, role_snapshot, city, country_name, latitude, longitude
    FROM school_loginactivity
    ORDER BY created_at DESC
''', conn)
```

For Supabase/PostgreSQL later, Streamlit can read the same table from PostgreSQL.

## Daily workflow

After pulling this update, run:

```powershell
git pull
.\start_server_windows.bat
```

The startup script runs migrations automatically, so `school_loginactivity` will be created.
