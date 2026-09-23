# Data cache

Downloaded Yahoo Finance CSV files are stored here so repeated research runs can use a local copy.

Workflow:
1. Run once with refresh enabled.
2. Inspect and freeze the CSV.
3. Record ticker, dates, git SHA and data hash.
4. Re-run without refresh for reproducibility.

Do not treat Yahoo Finance data as exchange-certified historical data. Validate corporate actions, missing bars and tradability before execution claims.
