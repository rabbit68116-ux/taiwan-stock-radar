# Agent Analyst Blueprint v1.1

Version: `v1.1`

Use this reference when designing the skill to behave like a senior Taiwan-equity analyst instead of a simple screener.

## 1. Objective

The agent should support two very different workloads:

1. Broad market sweep
   Scan roughly 1,800 TWSE and TPEX names and produce a ranked Top 20 shortlist with direction, setup type, buy zone, stop, and take-profit logic.
2. Single-stock deep dive
   When the user picks one stock, switch from fast ranking mode into a full research memo mode with stronger scenario analysis and action planning.

The critical design point is this:

- the 1,800-stock pass must be fast, standardized, and ruthlessly filter noise
- the single-stock pass must be deeper, slower, and thesis-driven

Do not use one template for both.

## 2. Operating modes

### Mode A: Market Sweep

Goal:
- compress the full universe into a small list of high-priority names

Inputs:
- daily price / volume
- liquidity
- sector
- chip flow
- monthly revenue and quality proxies
- market regime

Outputs:
- Top 20 shortlist
- sector summary
- signal distribution
- high-level action zones

### Mode B: Action Ranking

Goal:
- convert the shortlist into actionable watchlist names

Outputs must include:
- direction bias
- setup type
- buy zone
- stop loss
- take-profit ladder
- invalidation trigger
- confidence

### Mode C: Deep Dive

Goal:
- behave like a senior analyst writing a focused memo on one stock

This mode should not just repeat the scan result. It should re-open the thesis from multiple angles.

## 3. 1800-stock scanning architecture

Use a multi-stage pipeline:

### Stage 0: Data quality gate

Drop or penalize names with:
- stale data
- abnormal gaps in price history
- thin turnover
- suspicious single-day volume spikes

### Stage 1: Market regime map

Score the environment first:
- weighted index trend
- OTC trend
- turnover tone
- sector breadth
- volatility state

This stage sets the aggressiveness of the downstream engine.

### Stage 2: Sector rotation map

Before scoring stocks, rank sectors by:
- average relative strength
- breadth of participants
- volume expansion
- leadership persistence

Reason:
- strong names inside strong sectors usually deserve priority over isolated names

### Stage 3: Stock factor engine

Score each stock on:
- trend
- momentum
- volume confirmation
- liquidity
- foreign / trust / dealer flow
- financing and short structure
- revenue and quality proxies
- sector-relative strength
- regime fit

### Stage 4: Risk veto engine

Hard penalties for:
- low liquidity
- excessive volatility for the chosen horizon
- financing blow-off
- institutional distribution
- failed breakout structure
- weak sector context

### Stage 5: Action engine

For each stock, derive:
- direction bias
- setup type: breakout / trend pullback / early base
- buy zone
- stop
- TP1 / TP2
- what would invalidate the setup

### Stage 6: Portfolio shortlist engine

The Top 20 list should not be 20 copies of the same theme.

Apply diversification pressure:
- cap same-sector concentration
- prefer leaders over second-tier laggards
- avoid multiple names with identical risk drivers unless sector breadth is unusually strong

## 4. Top 20 output schema

Each ranked stock should have these fields:

| Field | Why it matters |
|---|---|
| Symbol / Name | Identification |
| Market / Sector | Context |
| Radar Score | Comparable ranking |
| Direction Bias | Uptrend continuation / constructive / neutral / defensive |
| Setup Type | Breakout, pullback, early base |
| Buy Zone | Where the setup becomes attractive |
| Stop Loss | Risk boundary |
| TP1 / TP2 | Planned exits or scale-out levels |
| Key Drivers | Why it ranks high |
| Main Risk Flag | Primary reason to be careful |
| Invalidation | What breaks the thesis |
| Confidence | Low / Medium / High |

## 5. Deep-dive framework for a single stock

When the user asks for a specific stock, the agent should switch from ranking mode to memo mode.

Required layers:

1. Market regime
2. Sector leadership and peer map
3. Business quality and revenue path
4. Chip flow and positioning
5. Multi-timeframe technical structure
6. Event calendar
7. Scenario tree
8. Action plan
9. Invalidation

### Market regime

Ask:
- is the broad tape helping or hurting this stock now?

### Sector and peer map

Compare against:
- top 3 direct peers
- sector median relative strength
- whether the stock is leading, confirming, or lagging the group

### Business quality and operating path

Go beyond price:
- monthly revenue trend
- EPS or margin direction
- product cycle or order-cycle positioning
- whether the current price move has business support

### Chip flow

Judge:
- foreign accumulation vs distribution
- trust support
- dealer behavior
- financing expansion and whether it is healthy or overheated

### Multi-timeframe technical structure

Check:
- daily trend
- weekly structure
- breakout base quality
- pullback depth
- key support / resistance / volume pivot

### Event calendar

List catalysts:
- monthly revenue release
- earnings
- ex-dividend
- major product launch
- policy or industry timing

### Scenario tree

Deep dive should always end with:

- base case
- bullish case
- bearish case
- trigger for each case
- probability bias

### Action plan

The action plan should include:
- ideal buy zone
- aggressive buy trigger
- conservative buy trigger
- stop
- first scale-out zone
- full failure condition

## 6. What makes the agent feel like a senior analyst

The agent should:

- prefer context over raw indicator dumping
- explain why a stock ranks above peers
- separate setup quality from business quality
- penalize fragile breakouts
- talk in scenarios, not promises
- always name what would make the current view wrong

What it should not do:

- output 20 bullish names from one overheated theme with no diversification logic
- give identical buy/sell language to every stock
- confuse ranking score with certainty
- skip liquidity or event timing

## 7. Recommended implementation phases

### Phase 1

Build the full-universe daily feature table for ~1,800 names.

### Phase 2

Add hierarchical ranking:
- market
- sector
- stock
- risk veto

### Phase 3

Add action-engine outputs:
- direction
- setup type
- buy zone
- stop
- TP ladder

### Phase 4

Add deep-dive stock memo mode:
- peer map
- catalyst calendar
- scenario tree
- confidence and invalidation

### Phase 5

Add feedback loop:
- track how Top 20 names behaved
- compare predicted setup type vs realized path
- recalibrate weights and action rules

## 8. Design conclusion

If this skill is meant to feel professional, the winning pattern is:

- universe scan for breadth
- sector map for context
- stock scoring for ranking
- action engine for entry/exit discipline
- deep-dive memo mode for conviction building

That is how the agent stops behaving like a stock screener and starts behaving like a real analyst.
