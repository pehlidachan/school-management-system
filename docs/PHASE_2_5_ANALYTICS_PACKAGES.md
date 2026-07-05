# Phase 2.5 Analytics Packages

This phase adds useful data/analytics packages for future reporting, Streamlit dashboards and Excel import/export.

## Added to requirements.txt

- `numpy`
- `pandas`
- `matplotlib`
- `seaborn`
- `openpyxl`

## Why these are useful

- `pandas`: tabular reports, CSV/Excel imports, fee/attendance analytics.
- `numpy`: numerical calculations behind analytics.
- `matplotlib`: charts for saved reports.
- `seaborn`: statistical/visual exploration for future dashboards.
- `openpyxl`: Excel file import/export support.

## Startup script update

`start_server_windows.bat` now installs requirements again automatically whenever `requirements.txt` is newer than `.requirements_installed`.

This keeps normal startup fast, but still installs new packages after a `git pull` when dependencies change.
