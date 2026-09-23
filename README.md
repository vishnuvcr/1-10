# 1-10 Quant Research - Final Daily Mean-Reversion Study

## Final status

The full research cycle is complete through Phase 7.

### Main empirical result

The locked 21-SMA / 14-RSI 10/90 gap-reversion rule is extremely sparse. NIFTY 50 in the 2010-2026 primary sample generated zero qualifying signals. Maximum-history testing across the fixed universe generated only 15 completed trades in total, with a maximum of 9 trades for any symbol. All inferential results are therefore descriptive-only.

The study does not establish a durable trading edge or production readiness.

## Manuscript

[Complete research manuscript](docs/RESEARCH_MANUSCRIPT.md)

[Research landing page](docs/index.md)

## Research evidence

[Research plan](docs/RESEARCH_PLAN.md)  
[Phase status](docs/PHASE_STATUS.md)  
[Error log](docs/ERROR_LOG.md)  
[Validation log](docs/VALIDATION_LOG.md)  
[Literature matrix](docs/LITERATURE_MATRIX.md)  
[Data source registry](docs/DATA_SOURCE_REGISTRY.md)

## Core implementation

[backtest.py](backtest.py)  
[requirements.txt](requirements.txt)  
[Unit tests](tests/test_backtest.py)

## Frozen results

[Maximum-history result artifacts](results/history_extension/)  
[Cost sensitivity grid](results/cost_sensitivity.csv)  
[Statistical validation](results/statistical_validation.csv)

## Reproducibility

Every research phase has a dedicated branch and documented status. GitHub Actions executes the code and stores the data/results artifacts. Raw-data manifests record SHA-256 hashes.

The next useful research experiment is not parameter optimization. It is a new preregistered study using intraday execution data and a directly tradable instrument with segment-accurate transaction costs.
