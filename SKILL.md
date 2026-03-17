---
name: taiwan-stock-radar
description: Use when the task is to build a Taiwan market brief, run a Taiwan stock scan, or analyze one Taiwan stock through a formal committee workflow. Start with the 08:30 daily brief when the user needs same-day Taiwan market direction, then move into the single-stock committee when deeper judgment is required. The v1.7 system also powers the Windows desktop app through the same shared Python core.
---

# taiwan-stock-radar

Current operating blueprint version: `v1.7`
Skill ID / repo slug: `taiwan-stock-radar`

Use this skill when the user wants a **Taiwan-equity research workflow that behaves like a disciplined desk process**, not a one-shot chatbot answer.

The `v1.7` default mode is:

- a daily `08:30` Taiwan market brief before the cash session
- one concise report with 10 key market messages and an overall day-session assessment
- one shared Python core used by the skill, CLI workflows, GitHub showcase, and Windows desktop app
- one stock at a time for deep-dive committee analysis when needed
- multiple specialist AI personas with explicit weights
- style-specific weighting for short-term, swing, and position analysis
- a final decision packet with scenarios, action levels, invalidation, and visible dissent

## Use this skill for

- daily Taiwan market brief generation before 09:00
- same-day Taiwan market direction assessment
- night-session and US spillover analysis
- Top20 demo scan generation
- single-stock analysis on TWSE or TPEX names
- deep-dive judgment on trend, momentum, price-volume, chip flow, fundamentals, and event risk
- buy zone, stop-loss, take-profit, invalidation, and style-aware robustness planning
- shared-core workflow design for both the skill route and the Windows desktop app

## Do not use this skill for

- guarantee-like return predictions
- broker execution or real-money automation
- intraday microstructure claims without fresh data
- shallow summaries that skip overnight context, liquidity, event timing, or chip flow
- generic macro commentary with no Taiwan-market application

## Read these references and configs only as needed

- `references/prediction-framework.md`
  Use when the user wants forecasts or scenario language that must stay honest about uncertainty.
- `references/agent-analyst-blueprint.md`
  Use when you need the multi-agent committee operating model and decision packet.
- `references/taiwan-indicator-framework-v1.7.md`
  Use when you need the Taiwan indicator stack, practical signal interpretation, or field-priority guidance.
- `references/daily-market-brief-framework-v1.7.md`
  Use when you need the `08:30` daily brief model, source mix, headline allocation, or reliability guardrails.
- `references/windows-desktop-framework-v1.7.md`
  Use when the task involves the Windows desktop delivery, GUI behavior, or packaging posture.
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
- `config/agent_personas.yaml`
  Use when you need role weights, specialties, or vote composition.
- `config/action_rules.yaml`
  Use when you need the required sections, scenario framework, and action-plan fields.

## Core workflow

1. Define the task.
   Confirm:
   - whether the user wants the daily market brief, the premarket brief, the Top20 scan, a single-stock memo, or several of these together
   - symbol and company name if a stock is specified
   - analysis date
   - style: `short_term`, `swing`, or `position` when a stock is involved
   - the exact user objective, such as same-day market outlook, buy point, or a full committee memo

2. Verify freshness.
   If the task depends on current price, revenue, news, or overnight moves, use fresh sources and state the exact date. If the evidence is stale or incomplete, reduce confidence.

3. Run the `08:30` daily market brief when relevant.
   Use it when:
   - the user asks before the Taiwan cash open
   - the user asks how Taiwan equities may trade today
   - the user wants overnight context before discussing any stock
   - a single-stock committee is requested for the same session and the daily brief is missing

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
   - `short_term`
   - `swing`
   - `position`

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

## Shared-core rule

`v1.7` must behave as one core with two delivery surfaces:

- the skill / CLI / docs route
- the Windows desktop route

Do not introduce analysis logic that only exists in one route unless it is clearly marked as display-only. Business logic belongs in `src/taiwan_stock_radar/`, not in the GUI layer.

## Default answer structure

For a full `v1.7` workflow, return:

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
- Treating a strong chart as enough when chip flow, event timing, or liquidity contradicts it
- Outputting buy or sell points without invalidation
- Presenting a strategy module without saying why it fits the active style
- Speaking as if the model can guarantee price direction
- Duplicating shared business logic inside the Windows app instead of calling the shared core

## Implementation posture

When converting this skill into code or workflows, favor:

- explicit `08:30` scheduling rules
- explicit source lists for Yahoo, Anue, and night-session inputs
- explicit indicator catalogs
- explicit style-weight profiles
- weighted-vote synthesis
- validation scorecards with mandatory sections
- outputs that can be reviewed, challenged, archived, and improved over time

This skill is successful when the final answer reads like a disciplined Taiwan-equity desk memo and the same workflow can be executed consistently from the CLI, the docs-backed skill flow, or the Windows desktop app.
