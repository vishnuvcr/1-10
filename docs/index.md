# 1-10 Quant Research

## Final status

Phase 7 complete.

### Main empirical finding

The locked 21-SMA / 14-RSI 10/90 daily gap-reversion rule is extremely sparse in the tested Indian-market universe. NIFTY 50 generated zero qualifying signals in the primary 2010-2026 sample, and the maximum-history diagnostic generated only 15 completed trades across five trade-bearing symbols.

The evidence does not establish a durable trading edge or production readiness.

## Research manuscript

[RESEARCH_MANUSCRIPT.md](RESEARCH_MANUSCRIPT.md)

## Core implementation

[backtest.py](../backtest.py)  
[requirements.txt](../requirements.txt)  
[tests/test_backtest.py](../tests/test_backtest.py)

## Research governance

[RESEARCH_PLAN.md](RESEARCH_PLAN.md)  
[PHASE_STATUS.md](PHASE_STATUS.md)  
[ERROR_LOG.md](ERROR_LOG.md)  
[VALIDATION_LOG.md](VALIDATION_LOG.md)  
[LITERATURE_MATRIX.md](LITERATURE_MATRIX.md)  
[DATA_SOURCE_REGISTRY.md](DATA_SOURCE_REGISTRY.md)

## Results

[Maximum-history results](../results/history_extension/)  
[Cost sensitivity](../results/cost_sensitivity.csv)  
[Statistical validation](../results/statistical_validation.csv)

## Future research

The next useful experiment is not parameter optimization. It is a new preregistered study using intraday execution data and a directly tradable instrument.
