# 1-10 Quant Research"éÝyø§yÔ Final Daily Mean-Reversion Study

## Final status

The research cycle is complete through Phase 7.

### Main empirical result

The locked 21-SMA / 14-RSI 10/90 gap-reversion rule is extremely sparse. NIFTY 50 in the 2010-2026 primary sample generated zero qualifying signals. Maximum-history testing across the fixed seven-symbol universe generated only 15 completed trades in total, with a maximum of 9 trades for any symbol. All symbol-level inferential results are therefore descriptive-only.

The study does not establish a durable trading edge or production readiness.

## Manuscript

[Complete research manuscript](docs/RESEARCH_MANUSCRIPT.md)

[Research landing page](docs/index.md)

## Research records

[Research plan](docs/RESEARCH_PLAN.md)  
[Phase status](docs/PHASE_STATUS.md)  
[Error log](docs/ERROR_LOG.md)  
[Validation log](docs/VALIDATION_LOG.md)  
[Literature matrix](docs/LITERATURE_MATRIX.md)  
[Data source registry](docs/DATA_SOURCE_REGISTRY.md)

## Core implementation

[Backtest engine](backtest.py)  
[Requirements](requirements.txt)  
[Unit tests](tests/test_backtest.py)

## Frozen results

[Maximum-history empirical results](results/history_extension/)  
[Cost sensitivity grid](results/cost_sensitivity.csv)  
[Statistical validation](results/statistical_validation.csv)

## Reproducibility

Every phase has a dedicated branch and an auditable workflow. Raw-data manifests record SHA-256 hashes. The research stops after Phase 7; parameter changes, regime filters and execution-model changes require a new preregistered study.

## Final interpretation

The most defensible conclusion is that the locked rule is too sparse for reliable robustness inference under the tested daily datasets and execution assumptions. The repository therefore does not promote it to live or production trading.

### Primary references

- Jegadeesh (1990), Journal of Finance, DOI 10.1111/j.1540-6261.1990.tb05110.x.
- Lehmann (1990), QJE, DOI 10.2307/2937816.
- White (2000), Econometrica, DOI 10.1111/1468-0262.00152.
- Bailey et al. (2017), Probability of Backtest Overfitting, DOI 10.21314/JCF.2016.322.
- Bailey & López de Prado (2014), Deflated Sharpe Ratio, DOI 10.2139/ssrn.2460551.
