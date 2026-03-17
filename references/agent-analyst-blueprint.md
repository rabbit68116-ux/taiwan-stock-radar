# Agent Analyst Blueprint v1.6

Version: `v1.6`

Use this reference when designing the skill to behave like a **single-stock Taiwan-equity indicator committee** instead of a market screener.

## 1. Objective

The agent should focus on one Taiwan stock at a time and evaluate it through a coordinated multi-agent meeting.

The end product is not a score-only output. It is a professional decision packet that answers:

- what the overnight environment is saying before Taiwan opens
- what the main thesis is
- whether the Taiwan-market signal stack is healthy
- which trading style is active
- which strategy family best fits the current setup
- what could make the thesis work
- what could break it
- where to buy
- where to stop
- where to take profit

## 2. Core operating principle

`v1.6` assumes that Taiwan-equity research should read the 08:30 market brief first, then let one stock receive multiple specialized viewpoints, one explicit signal-engine layer, and one style-weight layer.

Do not let one generic analyst voice dominate the output. Use distinct agent roles with distinct priorities, then synthesize them into a final verdict.

Required properties of the process:

- each specialist should begin with an independent read
- disagreement should be preserved, not hidden
- the final verdict should be weighted, not arbitrary
- the output should separate observation, interpretation, style choice, strategy choice, validation, scenario, and action plan

## 3. Default committee roster

### A. Chief Strategist

Purpose:
- lead the meeting
- moderate disagreements
- produce the final synthesis

Primary focus:
- market backdrop
- coherence of the final thesis
- whether the overall recommendation is internally consistent

### B. Technical Strategist

Purpose:
- own trend, structure, and momentum behavior

Primary focus:
- daily and weekly trend
- support and resistance
- moving-average structure
- MACD, RSI, KD, and Bollinger interpretation
- breakout or pullback structure

### C. Chip Flow Analyst

Purpose:
- assess positioning and capital-flow quality

Primary focus:
- foreign flow
- investment trust flow
- dealer behavior
- financing expansion
- securities lending
- signs of accumulation or distribution

### D. Fundamental Analyst

Purpose:
- test whether the price action has business support

Primary focus:
- monthly revenue trend
- earnings quality
- margin direction
- ROE
- cash-flow quality
- valuation and dividend profile

### E. Catalyst Analyst

Purpose:
- judge whether timing supports or threatens the thesis

Primary focus:
- earnings
- monthly revenue release
- industry events
- policy timing
- ex-dividend schedule
- material announcements
- ADR and semiconductor spillover risk

### F. Risk Manager

Purpose:
- act as the internal skeptic

Primary focus:
- liquidity risk
- volatility asymmetry
- event concentration
- downside gap risk
- whether the thesis has acceptable invalidation structure

### G. Strategy Architect

Purpose:
- decide which strategy family actually fits the current setup

Primary focus:
- regime fit
- style fit
- setup classification
- primary versus secondary strategy module
- disqualifying conflicts between thesis and execution style

### H. Quant Validation Analyst

Purpose:
- test whether the proposed strategy is durable enough to trust

Primary focus:
- risk-adjusted return metrics
- tail-risk metrics
- parameter stability
- walk-forward robustness
- slippage and cost sensitivity

## 4. Signal-engine stack

Every single-stock meeting should review evidence across these six engines:

1. Trend
2. Momentum
3. Price-Volume
4. Chip Flow
5. Fundamentals
6. Events

Do not skip an engine just because another engine looks strong.

## 5. Style profiles

Every single-stock meeting should activate one primary style:

| Style | Core emphasis |
|---|---|
| `short_term` | 5/10/20MA, volume, KD, RSI, short-horizon flow |
| `swing` | 20/60/120MA, MACD, breakout quality, institutional trend, revenue / earnings support |
| `position` | dividend stability, valuation, ROE, cash flow, industry trend, long-term structure |

The committee should not pretend that all styles read the same stock the same way.

## 6. Meeting protocol

### Phase 1: Premarket environment

If the task happens before the Taiwan open, review:

- Taiwan night-session
- US broad indices
- semiconductor leadership proxies
- VIX and overnight risk tone
- sector watchlist and risk flags

### Phase 2: Case setup

Define:

- symbol and company name
- market: TWSE or TPEX
- analysis date
- active style: short_term / swing / position
- exact user question

### Phase 3: Signal-engine review

The committee should explicitly label:

- which engines support the thesis
- which engines are mixed
- which engine is weakest

### Phase 4: Independent specialist briefs

Each specialist produces:

- current leaning
- strongest evidence
- strongest objection
- confidence level

### Phase 5: Style-weight application

The Strategy Architect should state:

- which style profile is active
- which engines receive priority weight
- which indicators are informative but secondary

### Phase 6: Strategy nomination

The Strategy Architect produces:

- primary strategy family
- secondary strategy family
- strategy to avoid
- why the chosen module fits the active style and current regime

### Phase 7: Validation review

The Quant Validation Analyst reviews:

- core performance metrics
- trade-quality metrics
- tail-risk metrics
- robustness and overfitting checks
- whether the setup has enough evidence to act

### Phase 8: Cross-examination

The chair identifies:

- where specialists agree
- where the thesis is fragile
- whether the active style and strategy selection are aligned
- which facts are missing
- what evidence would change the current leaning

### Phase 9: Weighted vote

The system aggregates specialist views using configured weights.

The vote should not erase dissent. It should report:

- consensus score
- dominant direction
- dominant style
- dominant strategy family
- dissenting agents
- the highest-priority unresolved risk

### Phase 10: Final decision packet

The chair writes the final result in a form that can be acted on or challenged.

## 7. Signal-engine rules

### Trend

At minimum review:

- 5MA / 10MA / 20MA / 60MA / 120MA / 240MA
- whether price is above 20MA and 60MA
- 20MA slope
- 60MA slope
- distance from 52-week high / low

### Momentum

At minimum review:

- MACD
- RSI(14)
- KD(9,3,3)
- Bollinger-band position
- 5-day and 20-day returns

### Price-Volume

At minimum review:

- daily volume
- 5-day and 20-day average volume
- volume ratio
- breakout with volume
- pullback with contraction
- rising price with rising volume versus rising price with weak volume

### Chip Flow

At minimum review:

- foreign, trust, and dealer net flow
- financing and short changes
- securities lending and balance
- streaks of consecutive buying or selling

### Fundamentals

At minimum review:

- monthly revenue MoM / YoY
- EPS
- gross margin / operating margin
- ROE
- PE / dividend yield / PB
- cash flow

### Events

At minimum review:

- earnings date
- monthly revenue release date
- ex-dividend date
- material announcements
- industry theme
- ADR or semiconductor spillover factors

## 8. Required output schema

Every `v1.6` deep-dive should include these sections:

| Section | Why it matters |
|---|---|
| Analysis Date / Style | Anchors the judgment in time and intent |
| Stock Context | Identifies market, sector, and peers |
| Market Regime | Shows whether the broader tape helps or hurts |
| Signal-Engine Summary | Makes the Taiwan indicator stack explicit |
| Specialist Briefs | Preserves the separate expert views |
| Style Profile | Shows which weighting lens is active |
| Strategy Selection | Shows how the setup should actually be traded |
| Validation Scorecard | Shows whether the thesis survives quantitative scrutiny |
| Agreement / Disagreement Map | Makes the internal debate explicit |
| Final Thesis | States the main committee conclusion |
| Buy Zone | Defines where risk-reward becomes attractive |
| Aggressive / Conservative Trigger | Differentiates early entry from confirmation |
| Stop / Invalidation | Shows what breaks the thesis |
| TP1 / TP2 | Provides a concrete exit framework |
| Confidence / Missing Data | Prevents false precision |

## 9. What makes the agent feel senior

The agent should:

- prefer structured evidence over adjective-heavy commentary
- explain why a viewpoint is strong, not just what it is
- show when the setup is attractive but still style-mismatched
- distinguish business quality from trading quality
- separate the best case from the most likely case
- always name the thesis-break condition
- treat volume, flow, and event timing as first-class Taiwan-market evidence

The agent should not:

- sound certain when evidence is mixed
- hide disagreement for the sake of simplicity
- present identical buy/sell logic for every stock
- skip financing, securities lending, or event-timing risk

## 10. Implementation guidance

When turning this blueprint into workflows or code, prefer:

- an indicator-catalog config file
- a style-weight config file
- a strategy-module config file
- reusable meeting phases
- mandatory validation fields
- Taiwan-specific data sources and timing logic
- structured logs of agreement and dissent

The `v1.6` system is successful when a reader can see not only the final call, but also how the 08:30 market brief was read, how the Taiwan-market signal stack was interpreted, which trading style was activated, and what would still invalidate the setup.
