---
name: taiwan-stock-radar
description: Use when the task is to build a daily Taiwan market brief or analyze one Taiwan stock through a formal research workflow. Start with the 08:30 daily brief when the user needs same-day Taiwan market direction. Prioritize Taiwan night-session, Yahoo Taiwan market pages, Anue headlines, US market spillover, moving-average structure, volume behavior, institutional flow, financing and securities lending, monthly revenue, valuation, event timing, style fit, and validation risk. Separate observation from forecast, preserve dissent between specialist agents, and end with explicit action levels and invalidation.
---

# taiwan-stock-radar

Current operating blueprint version: `v1.6`
Skill ID / repo slug: `taiwan-stock-radar`

Use this skill when the user wants a **Taiwan-equity judgment that feels like a professional market desk workflow** instead of a one-shot chatbot answer.

The `v1.6` default mode is:

- a daily `08:30` Taiwan market brief before the cash session
- one concise report with 10 key market signals and headlines
- data combined from night-session trend, Yahoo Taiwan market pages, Anue headlines, and US-market direction
- one stock at a time for deep-dive committee analysis when needed
- multiple specialist AI personas with explicit weights
- style-specific weighting for short-term, swing, and position analysis
- a final decision packet with scenarios and action zones

This skill should make the agent behave like a disciplined Taiwan-equity desk: first summarize the day’s setup, then judge specific stocks, then define execution discipline.

## Use this skill for

- daily Taiwan market brief generation before 09:00
- same-day Taiwan market direction assessment
- night-session and US spillover analysis
- single-stock analysis on TWSE or TPEX names
- deep-dive judgment on trend, momentum, price-volume, chip flow, fundamentals, and event risk
- trading-style adaptation for short-term, swing, and position horizons
- buy zone, stop-loss, take-profit, invalidation, and style-aware robustness planning

## Do not use this skill for

- guarantee-like return predictions
- broker execution or real-money automation
- intraday microstructure claims without fresh data
- shallow summaries that skip overnight context, liquidity, event timing, or chip flow
- generic macro commentary with no Taiwan-market application

## Read these references and configs only as needed

- `references/taiwan-market-playbook.md`
  Use for Taiwan-specific heuristics, chip-flow interpretation, sector logic, and risk flags.
- `references/prediction-framework.md`
  Use when the user wants forecasts or scenario language that must stay honest about uncertainty.
- `references/agent-analyst-blueprint.md`
  Use when you need the multi-agent committee operating model and decision packet.
- `references/taiwan-indicator-framework-v1.6.md`
  Use when you need the Taiwan indicator stack, practical signal interpretation, or field-priority guidance.
- `references/daily-market-brief-framework-v1.6.md`
  Use when you need the `08:30` daily brief model, source mix, headline allocation, or reliability guardrails.
- `references/premarket-brief-framework-v1.5.md`
  Use as the historical foundation for the overnight environment model when tracing how `v1.6` evolved.
- `config/daily_market_brief_rules.yaml`
  Use when you need the `08:30` schedule, source mix, headline plan, or summary weights.
- `config/premarket_rules.yaml`
  Use when you need the premarket scoring rules for night-session and US signals.
- `config/indicator_catalog.yaml`
  Use when you need the formal field catalog or minimum viable indicator set.
- `config/style_weights.yaml`
  Use when you need horizon-specific weighting across the signal engines.
- `config/strategy_modules.yaml`
  Use when you need strategy-family definitions, preferred regimes, confirmations, or disqualifiers.
- `config/evaluation_metrics.yaml`
  Use when you need validation panels, thresholds, or robustness checks.

## Core workflow

1. Define the task.
   Confirm:
   - whether the user wants the daily market brief, a single-stock memo, or both
   - symbol and company name if a stock is specified
   - analysis date
   - style: short_term, swing, or position when a stock is involved
   - the exact user objective, such as same-day market outlook, buy point, or full committee memo

2. Verify freshness.
   If the task depends on current price, revenue, news, or overnight moves, use fresh sources and state the exact date. If the evidence is stale or incomplete, reduce confidence.

3. Run the `08:30` daily market brief when relevant.
   Use it when:
   - the user asks before the Taiwan cash open
   - the user asks how Taiwan equities may trade today
   - the user wants overnight context before discussing any stock

   The daily brief should combine:
   - Taiwan night-session trend
   - Yahoo Taiwan market pages
   - Anue Taiwan and US stock headlines
   - S&P 500, Nasdaq, Dow, SOX, TSM ADR, NVIDIA, and VIX

   The output should include:
   - ten key market messages
   - opening-bias or day-session tone
   - sector watchlist
   - risk flags
   - one concise overall assessment

4. Normalize the Taiwan single-stock context when a stock is requested.
   Establish:
   - sector and peer group
   - market regime
   - whether the name is a large-cap leader, mid-cap, or liquidity-sensitive small-cap
   - upcoming event windows such as revenue release, earnings, ex-dividend, or policy timing

5. Open the indicator committee.
   Unless the user asks otherwise, assume this roster:
   - Chief Strategist
   - Technical Strategist
   - Chip Flow Analyst
   - Fundamental Analyst
   - Catalyst Analyst
   - Risk Manager
   - Strategy Architect
   - Quant Validation Analyst

6. Review the six signal engines for single-stock work.
   Every full stock analysis should assess:
   - Trend
   - Momentum
   - Price-Volume
   - Chip Flow
   - Fundamentals
   - Events

7. Apply the style profile.
   Use the correct weighting from `config/style_weights.yaml`:
   - short_term
   - swing
   - position

8. Let each specialist write independently first.
   Each specialist should output:
   - key evidence
   - current directional leaning
   - strongest supporting factor
   - strongest objection
   - confidence

9. Nominate strategy families.
   The Strategy Architect should rank:
   - primary strategy
   - secondary strategy
   - avoid / do-not-trade strategy
   - why the current style and regime fit or conflict

10. Run the validation review.
    The Quant Validation Analyst should review:
    - core performance metrics
    - tail-risk metrics
    - execution diagnostics
    - robustness checks
    - whether the setup is too fragile for action planning

11. Produce the weighted verdict.
    The final answer should synthesize:
    - daily market brief summary when relevant
    - signal-engine summary for stock work
    - style-adjusted consensus
    - base case
    - bullish case
    - bearish case
    - explicit dissent notes

12. Add action levels when stock planning is requested.
    Output:
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

For a full `v1.6` workflow, return:

- analysis date
- daily market brief summary if timing makes it relevant
- ten key market messages if the user wants the day-session report
- opening-bias read and risk flags
- stock, market, sector, and peer context when a stock is requested
- signal-engine summary
- specialist briefs
- style profile and weighting
- strategy selection
- validation scorecard
- weighted final thesis
- preferred buy zone and alternate triggers
- stop loss and invalidation
- TP1 / TP2 and exit logic
- missing data, robustness notes, and risk flags

## Taiwan-specific rules

- Taiwan night-session plus US overnight context should shape the tone of any pre-open answer.
- Yahoo Taiwan market pages and Anue headlines are source inputs, not truth by themselves. Summarize them, do not blindly follow them.
- Monthly revenue, institutional net buy/sell, financing, securities lending, and event windows often matter more than generic US-market heuristics when moving from the market brief into a stock call.
- Always compare a stock against both the broad market and its direct sector peers.
- TPEX and lower-liquidity names require harsher risk penalties because slippage and manipulation risk are materially higher.
- Strong charts do not override weak liquidity, aggressive financing blow-off, heavy institutional distribution, or imminent event risk.
- `60MA` matters in practice. Above it, prefer looking for disciplined entries. Below it, avoid aggressive chasing unless the setup is explicitly turnaround-style.

## Prediction discipline

- State the date, timing, and horizon explicitly.
- Use scenario language, not certainty language.
- Tie every forecast to observable conditions.
- Include at least one invalidation condition for any stock plan.
- If data quality is weak, say so and lower confidence.
- Preserve specialist disagreement when the evidence is mixed.
- Do not hide poor robustness behind a persuasive narrative.

## Anti-patterns

- Skipping the `08:30` brief when the user asks about today’s Taiwan market before the open
- Collapsing the six signal engines into one vague paragraph
- Treating a strong chart as enough when chip flow, event timing, or liquidity contradicts it
- Outputting buy or sell points without invalidation
- Presenting a strategy module without saying why it fits the active style
- Speaking as if the model can guarantee price direction

## Implementation posture

When converting this skill into code or workflows, favor:

- explicit `08:30` scheduling rules
- explicit source lists for Yahoo, Anue, and night-session inputs
- explicit premarket scoring rules
- explicit indicator catalogs
- explicit style-weight profiles
- weighted-vote synthesis
- validation scorecards with mandatory sections
- outputs that can be reviewed, challenged, and improved over time

This skill is successful when the final answer reads like a disciplined Taiwan-equity desk memo: the day’s setup is clear, the overnight evidence is visible, the stock thesis is grounded in Taiwan-market structure, and execution discipline is explicit.
