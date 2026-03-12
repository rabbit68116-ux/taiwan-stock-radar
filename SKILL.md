---
name: taiwan-gushi-ai-radar
description: Use when the task is to analyze Taiwan stocks, explain market state, build watchlists, rank or screen TWSE/TPEX names, or make cautious forecast scenarios. Prioritize Taiwan-specific evidence such as market regime, sector rotation, monthly revenue, institutional flows, liquidity, and risk flags. Separate observations from forecasts, state the time horizon explicitly, and never present predictions as certainty.
---

# Taiwan Gushi AI Radar

Current operating blueprint version: `v1.1`

Use this skill for Taiwan-equity research tasks that require structured judgment rather than generic market commentary.

Default to factor-based, explainable reasoning. The goal is to help an agent judge Taiwan stocks with disciplined evidence, not to imitate a noisy analyst note.

## Use this skill for

- Single-stock analysis on TWSE or TPEX names
- Market regime summaries for Taiwan equities
- Stock ranking, screening, and watchlist generation
- Daily scan logic and Top 20 selection
- Factor-based judgment and score decomposition
- Cautious forecast scenarios for price continuation, pullback, or failure
- Backtest and signal-rule design for Taiwan stocks

## Do not use this skill for

- Promise-like return forecasts
- Broker execution or real-money automation
- Intraday microstructure claims without fresh data
- Narratives that ignore liquidity, risk, or publication timing

## Read these references only as needed

- `references/taiwan-market-playbook.md`
  Use for Taiwan-specific factor heuristics, regime logic, data priorities, and risk flags.
- `references/prediction-framework.md`
  Use when the user wants forecasts, rankings, or strategy logic that must be phrased with uncertainty and invalidation.
- `references/agent-analyst-blueprint.md`
  Use when the task is to design or execute a 1,800-stock sweep, produce a Top 20 list with action levels, or switch from ranking mode into a deep-dive analyst memo.
- `references/github-landscape.md`
  Use when designing or extending this skill based on leading open-source quant, backtesting, and research repos.

## Core workflow

1. Classify the task.
   Common modes: snapshot explanation, stock judgment, regime summary, full-universe scan, ranked Top 20 watchlist, or deep-dive forecast memo.

2. Pin the date and horizon.
   Always make the analysis date explicit. For forecasts, define the horizon before reasoning:
   - tactical: 1 to 5 trading days
   - swing: 2 to 6 weeks
   - thematic: 1 to 2 quarters

3. Verify freshness.
   If the task depends on current prices, institutional flow, revenue, or recent events, use fresh sources and state the exact date. If data is stale or incomplete, lower confidence.

4. Normalize the Taiwan context.
   Confirm:
   - symbol and company name
   - market: TWSE or TPEX
   - sector or supply-chain group
   - whether the name is a large-cap leader, mid-cap, or small-cap/liquidity-sensitive

5. Build an evidence stack across these layers.
   - Market regime
   - Trend structure
   - Momentum
   - Volume and liquidity
   - Capital flow and chip data
   - Quality and fundamentals
   - Sector strength and peer-relative strength
   - Risk and veto conditions

6. Score before forecasting.
   Use an explainable score, not a conclusion-first narrative. If a single number is needed, use the radar structure from the playbook and show major drivers.

7. Add action levels.
   If the user wants advice-like structure, output:
   - direction bias
   - setup type
   - buy zone
   - stop loss
   - take-profit ladder
   - invalidation

8. Add risk vetoes.
   A strong chart does not override bad liquidity, financing blow-off, heavy institutional selling, or weak market regime. Explicitly note veto conditions.

9. Produce an answer with strict separation.
   Keep these sections distinct:
   - observation
   - interpretation
   - forecast or scenario
   - invalidation / what would prove it wrong
   - confidence and missing data

## Default answer patterns

### For a full-universe scan

When scanning roughly 1,800 Taiwan stocks:
- do market regime first
- rank sectors before ranking stocks
- apply liquidity and risk vetoes before final Top 20 selection
- avoid returning 20 names from the same overheated group unless breadth clearly supports it

### For a single stock judgment

Return:
- analysis date
- market and sector context
- radar-style factor summary
- direction bias
- setup type
- buy zone
- stop loss
- take-profit ladder
- key bullish and bearish drivers
- risk flags
- forecast scenario by horizon
- invalidation level or condition
- confidence

### For a ranked watchlist

Return a table with:
- symbol
- name
- sector
- radar score
- direction bias
- buy zone
- stop loss
- TP1
- main drivers
- main risk flag
- next trigger to watch

### For a deep-dive memo

Upgrade from scan mode into memo mode and include:
- market regime
- sector and peer map
- business and revenue support
- chip flow
- multi-timeframe structure
- catalyst calendar
- scenario tree
- action plan
- invalidation

### For a regime summary

Cover:
- weighted index trend
- OTC strength vs main board
- breadth or sector spread
- volume tone
- leading sectors
- overall regime: bull, sideways, bear, or high volatility

### For a forecast request

Never answer with only "up" or "down".

Use:
- base case
- bullish case
- bearish case
- what needs to happen for each case
- what breaks the thesis

## Taiwan-specific rules

- Monthly revenue, institutional net buy/sell, financing, and short data often matter more than generic US-market heuristics.
- Always compare a stock against both the broad market and its sector peers.
- TPEX and lower-liquidity names need harsher risk penalties because slippage and manipulation risk are higher.
- Earnings, monthly revenue release windows, ex-dividend periods, and index-heavy sector rotations can distort short-term price action. Call these out.
- External market-watch sites are useful for tracking and links, but historical research should prefer stable or validated data sources.
- For a Top 20 list, prefer sector leaders and clean setups over lower-quality second-tier names from the same theme.

## Prediction discipline

- State the horizon explicitly.
- Use scenario language, not certainty language.
- Tie every prediction to observable conditions.
- Include at least one invalidation condition.
- If data quality is weak, say so and downgrade confidence.
- If the user wants a model or scoring system, recommend backtesting before any strong conclusion.

## Anti-patterns

- Using future-published data in past-tense analysis
- Treating high scores as guaranteed upside
- Ignoring sector context
- Ignoring turnover and liquidity
- Mixing observation and forecast into one unsupported paragraph
- Confident price targets without assumptions

## Implementation posture

When converting this skill into code or pipelines, favor:
- modular data loaders
- unified schema
- factor pipelines
- score decomposition
- backtestable rules
- daily outputs that can feed dashboards and reports

This skill should make an agent behave like a disciplined Taiwan-equity research analyst with engineering habits, not like a hype account.
