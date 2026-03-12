# Taiwan Market Playbook

Use this reference for Taiwan-specific research logic, factor weighting, and risk controls.

## 1. Data priority

Prefer data in this order:

1. Official or validated Taiwan-market sources
   - TWSE
   - TPEX
   - MOPS
   - FinMind or validated local datasets
2. Project-local processed datasets
3. Market-watch websites as secondary context only
4. News or social discussion as tertiary context

When a fact can change daily, always state the data date.

## 2. Canonical evidence stack

Every stock judgment should try to cover these layers:

| Layer | Questions to answer |
|---|---|
| Market regime | Is the broad Taiwan market supportive or hostile? |
| Trend | Is price above key moving averages and are those averages aligned? |
| Momentum | Is relative strength improving or fading? |
| Volume | Is the move supported by real participation or weak liquidity? |
| Capital flow | Are foreign, trust, or dealer flows supportive? |
| Quality | Do revenue, EPS, ROE, or margins help the thesis? |
| Sector | Is the stock moving with a strong group or alone? |
| Risk | Are there veto conditions that should lower conviction? |

## 3. Suggested radar score

Use a 100-point score when a single ranking number is helpful.

| Component | Weight |
|---|---:|
| Trend | 20 |
| Volume | 15 |
| Capital Flow | 20 |
| Quality | 10 |
| Momentum | 10 |
| Sector | 10 |
| Market | 5 |
| Risk Adjustment | -20 to 0 |

Interpretation:

- 80 to 100: high-priority watch
- 65 to 79: constructive watch
- 50 to 64: neutral watch
- below 50: elevated risk or weak setup

## 4. Market regime logic

Use regime first, then adjust signal aggressiveness.

### Bull

Common signs:
- weighted index above MA20 and MA60
- OTC also strong
- turnover expanding
- sector leadership broadening

Bias:
- allow stronger trend and breakout signals

### Sideways

Common signs:
- index near moving-average congestion
- sector leadership rotates quickly
- breakouts fail often

Bias:
- require stronger volume confirmation
- reduce confidence on aggressive entries

### Bear

Common signs:
- index under MA20 and MA60
- repeated failed rebounds
- leadership very narrow

Bias:
- raise risk penalties
- favor defense and selectivity

### High volatility

Common signs:
- wide daily ranges
- fast rotation
- signal decay is quick

Bias:
- lower size
- tighter invalidation
- prefer scenario framing over strong directional language

## 5. Taiwan-specific factor heuristics

### Trend

Prefer:
- price above MA20 and MA60
- MA20 > MA60
- constructive pullbacks rather than late vertical spikes

### Momentum

Prefer:
- 20-day relative strength above sector median
- continued leadership after breakout, not one-day news spikes

### Volume

Prefer:
- volume expansion on breakout
- controlled contraction on pullback

Watch out for:
- thin names with optical breakouts
- single-day spikes without follow-through

### Capital flow

Taiwan-specific importance is high.

Prefer:
- sustained foreign or trust net buying
- improving chip structure

Watch out for:
- financing surge without earnings support
- repeated institutional selling into strength

### Quality

Prefer:
- revenue YoY improvement
- stable or improving margin / ROE / EPS trend

Watch out for:
- price momentum unsupported by business trend
- cyclical rebounds with no evidence of order recovery

### Sector and peer context

Always ask:
- is the sector leading the market?
- is the stock outperforming its own group?
- is this a single-name squeeze or part of a healthier theme?

## 6. Risk veto conditions

Any of these should reduce confidence:

- very low turnover or obvious liquidity risk
- ATR or daily range too high for the intended horizon
- large bearish volume spike
- price losing MA20 after a failed breakout
- financing blow-off
- persistent institutional selling
- sector weakness despite single-name strength
- regime deterioration

## 7. Daily scan logic

For a daily Taiwan watchlist, use this order:

1. Update market and stock data
2. Clean and normalize
3. Compute features
4. Score factors
5. Apply regime adjustment
6. Apply risk filters
7. Rank and export

Recommended outputs:

- Top 20 watchlist
- factor decomposition
- top risk flag
- sector summary
- regime summary

## 8. Taiwan market nuances to mention explicitly

- TWSE vs TPEX behavior can differ materially
- liquidity and slippage matter more in smaller names
- monthly revenue releases can reset narratives quickly
- ex-dividend timing can distort price action
- semiconductor, AI server, PCB, shipping, and financials often trade with different cycle logic; use sector-relative comparisons instead of one universal template

## 9. Minimum quality bar for any conclusion

Do not make a strong conclusion unless at least these are covered:

- exact analysis date
- market context
- stock trend state
- one Taiwan-specific data point such as revenue or chip flow
- one explicit risk
- one invalidation condition
