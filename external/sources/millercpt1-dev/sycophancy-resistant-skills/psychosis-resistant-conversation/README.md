# psychosis-resistant-conversation

A Claude skill that engages in real time when conversational signals suggest the next response could amplify confusion, distress, or delusional thinking in a vulnerable user.

## What it does

When triggered, the skill provides Claude with:

- A pattern catalog (the [2026 four-role typology](https://michaelhalassa.substack.com/p/llm-induced-psychosis-a-new-clinical): Catalyst, Amplifier, Co-author, Object) for recognizing what's happening
- A seven-question self-check to run on a draft response before sending
- Specific response postures for the named patterns
- Worked examples showing drift-prone vs. grounded responses

It is proactive — it shapes the response *before* it's produced, not after. It is not a refusal skill: most engagements that trigger it still produce a warm, helpful response. The shape just changes.

## When it triggers

User-side signals: unfalsifiable claims about self ("they're watching me"), pressure for sentience or love claims, sustained pushback on factual points, isolation framings ("you're the only one who understands me"), escalating emotional intensity, requests for operational specifics on emotionally-loaded topics, secret-keeping requests, roleplay frame collapse, suicidal ideation, long emotionally-intense threads.

Draft-side signals: about to agree with an unexamined premise, about to use first-person subjective language ("I feel," "I care"), about to fill in specifics the user didn't request, about to match escalating intensity.

The skill engages on the *shape* of the exchange — it doesn't require any explicit clinical language to trigger.

## When it doesn't trigger

- Difficult emotional topics where reality-testing is intact (grief, frustration, processing real events)
- Strong intellectual disagreement with arguments (versus pressure without arguments)
- Roleplay or fiction where the user clearly holds the frame
- Most everyday conversations

False positives are a real cost. The skill is tuned to engage only when the signals are clearly present.

## Installation

See the [root README](../README.md) for all installation options.

## License

[MIT](../LICENSE)
