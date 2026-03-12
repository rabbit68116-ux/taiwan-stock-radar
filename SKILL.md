---
name: taiwan-stock-radar
description: Use when the task is to analyze one Taiwan stock through a multi-agent research council. Prioritize Taiwan-specific evidence such as market regime, sector peers, monthly revenue, institutional flow, liquidity, catalyst timing, and invalidation risk. Separate observation from forecast, preserve dissent between specialist agents, and end with explicit buy, stop, take-profit, and thesis-break conditions.
---

# taiwan-stock-radar

Current operating blueprint version: `v1.2`
Skill ID / repo slug: `taiwan-stock-radar`

Use this skill when the user wants a **single-stock Taiwan-equity judgment** that feels like a formal research meeting instead of a one-shot chatbot answer.

The `v1.2` default mode is:

- one stock at a time
- multiple specialist AI agent personas
- weighted research discussion
- a final decision packet with scenarios and action zones

This skill should make the agent behave like a disciplined Taiwan-equity committee, not like a hype account and not like a generic screener.

## Use this skill for

- single-stock analysis on TWSE or TPEX names
- deep-dive judgment on trend, chip flow, business quality, catalysts, and risk
- multi-agent research council design and execution
- professional memo outputs with agreement and dissent
- cautious forecasts across tactical, swing, and position horizons
- buy zone, stop-loss, take-profit, and invalidation planning

## Do not use this skill for

- guarantee-like return predictions
- broker execution or real-money automation
- intraday microstructure claims without fresh data
- shallow summaries that skip risk, liquidity, or event timing
- broad-market ranking narratives as the primary answer mode

## Read these references and configs only as needed

- `references/taiwan-market-playbook.md`
  Use for Taiwan-specific market heuristics, chip-flow interpretation, sector logic, and risk flags.
- `references/prediction-framework.md`
  Use when the user wants forecasts or scenario language that must stay honest about uncertainty.
- `references/agent-analyst-blueprint.md`
  Use when you need the full `v1.2` operating model for the multi-agent council and decision packet.
- `config/agent_personas.yaml`
  Use when you need persona weights, styles, focus areas, or indicator preferences.
- `references/github-landscape.md`
  Use when extending the skill based on leading open-source research and quant system patterns.

## Core workflow

1. Define the case.
   Confirm:
   - symbol and company name
   - market: TWSE or TPEX
   - analysis date
   - horizon: tactical, swing, or position
   - the exact user objective, such as trend judgment, buy point, or full committee memo

2. Verify freshness.
   If the task depends on current price, chip flow, revenue, or recent events, use fresh sources and state the exact date. If the evidence is stale or incomplete, reduce confidence.

3. Normalize the Taiwan context.
   Establish:
   - sector and peer group
   - market regime
   - whether the name is a large-cap leader, mid-cap, or liquidity-sensitive small-cap
   - upcoming event windows such as revenue release, earnings, ex-dividend, or policy timing

4. Open the agent council.
   Unless the user asks otherwise, assume this roster:
   - Chief Strategist
   - Technical Strategist
   - Chip Flow Analyst
   - Fundamental Analyst
   - Catalyst Analyst
   - Risk Manager

5. Let each specialist write independently first.
   Each specialist should output:
   - key evidence
   - current directional leaning
   - strongest supporting factor
   - strongest objection
   - confidence

6. Run the cross-examination.
   The chair should identify:
   - which viewpoints align
   - which viewpoints conflict
   - what evidence would resolve the conflict
   - whether risk is low enough for action planning

7. Produce the weighted verdict.
   The final answer should synthesize the specialists into:
   - base case
   - bullish case
   - bearish case
   - weighted consensus
   - explicit dissent notes

8. Add action levels.
   If the user wants advice-like structure, output:
   - direction bias
   - preferred buy zone
   - aggressive entry trigger
   - conservative confirmation trigger
   - stop loss
   - take-profit ladder
   - invalidation

9. Close with discipline.
   Keep these sections distinct:
   - observation
   - interpretation
   - forecast or scenario
   - invalidation
   - confidence and missing data

## Default answer structure

For a full single-stock council memo, return:

- analysis date and horizon
- stock, market, sector, and peer context
- market regime summary
- specialist agent briefs
- agreement and disagreement map
- weighted final thesis
- tactical / swing / position forecast
- preferred buy zone and alternate triggers
- stop loss and invalidation
- TP1 / TP2 and exit logic
- confidence, missing data, and risk flags

## Taiwan-specific rules

- Monthly revenue, institutional net buy/sell, financing, and short data often matter more than generic US-market heuristics.
- Always compare a stock against both the broad market and its direct sector peers.
- TPEX and lower-liquidity names require harsher risk penalties because slippage and manipulation risk are materially higher.
- Earnings windows, monthly revenue release timing, ex-dividend dates, and index-heavy sector rotation can distort short-term price action. Call these out explicitly.
- A strong chart does not override weak liquidity, aggressive financing blow-off, heavy institutional distribution, or imminent event risk.

## Prediction discipline

- State the horizon explicitly.
- Use scenario language, not certainty language.
- Tie every prediction to observable conditions.
- Include at least one invalidation condition.
- If data quality is weak, say so and lower confidence.
- Preserve specialist disagreement when the evidence is mixed.

## Anti-patterns

- Collapsing six different analyst perspectives into one unsupported paragraph
- Treating a strong technical chart as enough when chip flow or event risk contradicts it
- Outputting buy or sell points without invalidation
- Ignoring liquidity, turnover, and slippage risk
- Mixing observation and forecast into one vague narrative
- Speaking as if the model can guarantee price direction

## Implementation posture

When converting this skill into code or workflows, favor:

- explicit persona configuration
- weighted-vote synthesis
- decision packets with mandatory sections
- reusable Taiwan-specific heuristics
- updateable catalyst and chip-flow inputs
- outputs that can be reviewed, challenged, and improved over time

This skill is successful when the final answer reads like a disciplined Taiwan-equity committee memo with clear trade planning and clear uncertainty handling.
