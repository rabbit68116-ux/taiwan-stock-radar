---
name: taiwan-stock-radar
description: Use when the task is to analyze one Taiwan stock through an indicator-driven multi-agent research committee. Prioritize Taiwan-specific evidence such as moving-average structure, volume behavior, institutional flow, financing and securities lending, monthly revenue, valuation, event timing, style fit, and validation risk. Separate observation from forecast, preserve dissent between specialist agents, and end with explicit buy, stop, take-profit, invalidation, and style-weight notes.
---

# taiwan-stock-radar

Current operating blueprint version: `v1.4`
Skill ID / repo slug: `taiwan-stock-radar`

Use this skill when the user wants a **single-stock Taiwan-equity judgment** that feels like a formal research meeting built on Taiwan-market signal engines and style-specific weighting, instead of a one-shot chatbot answer.

The `v1.4` default mode is:

- one stock at a time
- multiple specialist AI personas
- explicit signal-engine review
- style-specific weighting for short-term, swing, and position analysis
- strategy-family selection after signal review
- a final decision packet with scenarios and action zones

This skill should make the agent behave like a disciplined Taiwan-equity indicator committee, not like a hype account and not like a generic screener.

## Use this skill for

- single-stock analysis on TWSE or TPEX names
- deep-dive judgment on trend, momentum, price-volume, chip flow, fundamentals, and event risk
- trading-style adaptation for short-term, swing, and position horizons
- strategy-family selection for a specific setup
- professional memo outputs with agreement and dissent
- buy zone, stop-loss, take-profit, invalidation, and style-aware robustness planning

## Do not use this skill for

- guarantee-like return predictions
- broker execution or real-money automation
- intraday microstructure claims without fresh data
- shallow summaries that skip liquidity, event timing, or chip flow
- broad-market ranking narratives as the primary answer mode

## Read these references and configs only as needed

- `references/taiwan-market-playbook.md`
  Use for Taiwan-specific market heuristics, chip-flow interpretation, sector logic, and risk flags.
- `references/prediction-framework.md`
  Use when the user wants forecasts or scenario language that must stay honest about uncertainty.
- `references/agent-analyst-blueprint.md`
  Use when you need the full `v1.4` operating model for the multi-agent committee and decision packet.
- `references/taiwan-indicator-framework-v1.4.md`
  Use when you need the Taiwan indicator stack, practical signal interpretation, or field-priority guidance.
- `config/indicator_catalog.yaml`
  Use when you need the formal field catalog, source intent, or minimum viable indicator set.
- `config/style_weights.yaml`
  Use when you need horizon-specific weighting across the signal engines.
- `config/strategy_modules.yaml`
  Use when you need the strategy-family definitions, preferred regimes, confirmations, or disqualifiers.
- `config/evaluation_metrics.yaml`
  Use when you need the reporting metrics, thresholds, validation panels, or robustness checks.

## Core workflow

1. Define the case.
   Confirm:
   - symbol and company name
   - market: TWSE or TPEX
   - analysis date
   - style: short_term, swing, or position
   - the exact user objective, such as trend judgment, buy point, or full committee memo

2. Verify freshness.
   If the task depends on current price, chip flow, revenue, or recent events, use fresh sources and state the exact date. If the evidence is stale or incomplete, reduce confidence.

3. Normalize the Taiwan context.
   Establish:
   - sector and peer group
   - market regime
   - whether the name is a large-cap leader, mid-cap, or liquidity-sensitive small-cap
   - upcoming event windows such as revenue release, earnings, ex-dividend, or policy timing

4. Open the indicator committee.
   Unless the user asks otherwise, assume this roster:
   - Chief Strategist
   - Technical Strategist
   - Chip Flow Analyst
   - Fundamental Analyst
   - Catalyst Analyst
   - Risk Manager
   - Strategy Architect
   - Quant Validation Analyst

5. Review the signal engines first.
   Every full analysis should assess:
   - Trend
   - Momentum
   - Price-Volume
   - Chip Flow
   - Fundamentals
   - Events

6. Apply the style profile.
   Use the correct weighting from `config/style_weights.yaml`:
   - short_term
   - swing
   - position

7. Let each specialist write independently first.
   Each specialist should output:
   - key evidence
   - current directional leaning
   - strongest supporting factor
   - strongest objection
   - confidence

8. Nominate strategy families.
   The Strategy Architect should rank the best-fit modules for the case:
   - primary strategy
   - secondary strategy
   - avoid / do-not-trade strategy
   - why the current style and regime fit or conflict

9. Run the validation review.
   The Quant Validation Analyst should review:
   - core performance metrics
   - tail-risk metrics
   - execution diagnostics
   - robustness checks
   - whether the setup is too fragile for action planning

10. Run the cross-examination.
   The chair should identify:
   - which viewpoints align
   - which viewpoints conflict
   - which engine is weakest
   - what evidence would resolve the conflict
   - whether the setup clears the minimum validation bar

11. Produce the weighted verdict.
   The final answer should synthesize the specialists into:
   - signal-engine summary
   - style-adjusted consensus
   - base case
   - bullish case
   - bearish case
   - explicit dissent notes

12. Add action levels.
   If the user wants advice-like structure, output:
   - direction bias
   - active style profile
   - primary strategy module
   - preferred buy zone
   - aggressive entry trigger
   - conservative confirmation trigger
   - stop loss
   - take-profit ladder
   - invalidation
   - do-not-trade condition

## Default answer structure

For a full `v1.4` single-stock committee memo, return:

- analysis date and style
- stock, market, sector, and peer context
- market regime summary
- signal-engine summary
- specialist briefs
- style profile and weighting
- strategy selection
- validation scorecard
- agreement and disagreement map
- weighted final thesis
- preferred buy zone and alternate triggers
- stop loss and invalidation
- TP1 / TP2 and exit logic
- robustness notes, missing data, and risk flags

## Taiwan-specific rules

- Monthly revenue, institutional net buy/sell, financing, securities lending, and event windows often matter more than generic US-market heuristics.
- Always compare a stock against both the broad market and its direct sector peers.
- TPEX and lower-liquidity names require harsher risk penalties because slippage and manipulation risk are materially higher.
- Strong charts do not override weak liquidity, aggressive financing blow-off, heavy institutional distribution, or imminent event risk.
- `60MA` matters in practice. Above it, prefer looking for disciplined entries. Below it, avoid aggressive chasing unless the setup is explicitly turnaround-style.
- `KD` and `RSI` are useful, but neither should be used alone as a sell or short trigger in strong Taiwan-equity leadership names.

## Prediction discipline

- State the style and horizon explicitly.
- Use scenario language, not certainty language.
- Tie every prediction to observable conditions.
- Include at least one invalidation condition.
- If data quality is weak, say so and lower confidence.
- Preserve specialist disagreement when the evidence is mixed.
- Do not hide poor robustness behind a persuasive narrative.

## Anti-patterns

- Collapsing the six signal engines into one vague paragraph
- Treating a strong chart as enough when chip flow, event timing, or liquidity contradicts it
- Outputting buy or sell points without invalidation
- Ignoring securities lending, financing stress, or event density
- Presenting a strategy module without saying why it fits the active style
- Speaking as if the model can guarantee price direction

## Implementation posture

When converting this skill into code or workflows, favor:

- explicit indicator catalogs
- explicit style-weight profiles
- explicit strategy-family definitions
- weighted-vote synthesis
- validation scorecards with mandatory sections
- updateable Taiwan-specific event and chip-flow inputs
- outputs that can be reviewed, challenged, and improved over time

This skill is successful when the final answer reads like a disciplined Taiwan-equity indicator committee memo with clear trade planning, visible uncertainty, and style-aware signal interpretation.
