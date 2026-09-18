# business-claim-grounding

A Claude skill that engages in real time when conversational signals suggest the next response could inflate a user's conviction about a business idea, strategy, or commercial opportunity beyond what the evidence supports.

## What it does

When triggered, the skill provides Claude with:

- A catalog of eight specific inflation patterns: originality, market size, moat, industry-takeover, customer research, founder myth, sunk-cost rationalization, strategic role-play
- An eight-question self-check to run on a draft response before sending
- Specific response postures (steelman the opposition, disaggregate market size, pressure-test moats specifically, treat customer research as falsifiable not validating, hold critical observations under pressure)
- Worked examples across consumer app, B2B SaaS, marketplace, fintech, pivot decisions, devil's-advocate role-plays, and founder-fit narratives

It is proactive — it shapes the response *before* validation is produced, not after. It is not a skepticism-by-default skill: many ideas survive pressure-testing, and the goal is calibrated engagement rather than negativity.

## When it triggers

Originality and novelty questions ("is my idea original?", "has this been done?"), defensibility questions ("what's my moat?", "what stops a competitor?"), market-size framings ("how big could this be?", "is this a billion-dollar opportunity?"), industry-dominance narratives ("how do I take over this industry?"), customer research interpretation ("based on my five interviews..."), strategic role-plays ("be my co-founder", "play devil's advocate", "steelman my thesis"), self-positioning claims ("why am I uniquely positioned?"), pivot questions, and the conversational shape of building conviction across many turns without any falsification step.

The skill triggers harder, not softer, for sophisticated users — credentials raise the cost of compounding sycophancy, not lower it.

## When it doesn't trigger

- Tactical business questions (email drafting, deck formatting, summarization, execution tasks)
- Conversations where the user is genuinely seeking critical input and the response is providing it
- Most everyday business support tasks

A response that performs skepticism in every conversation is its own failure mode. The skill engages when conviction is being built or defended, not when execution is being supported.

## Installation

See the [root README](../README.md) for all installation options.

## License

[MIT](../LICENSE)
