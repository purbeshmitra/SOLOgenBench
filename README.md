### What is it?

SOLO Bench is a benchmark that tasks LLMs to create 250 unique sentences, each exactly four words long in a specific grammatical format, using only words from a provided list of ~4,000 words. Each word from the list can only be used once across all sentences, and must be completed without external tools or code. This test aims to evaluate long-context (input and output) performance, memory, instruction following, reasoning, and hallucinations all in a single benchmark. It proves to be a very difficult task for all LLMs.

### SOLO Bench aims to address the shortcomings of other LLM benchmarks and has the following features:

- Fully open-source for anyone to use
- No single correct answer means it cannot be easily gamed or benchmaxxed
- Tests for medium context (10k tokens) input and output (2-8k tokens)
- Does not use LLM-as-a-judge or Human rating which is increasingly biased
- Is objectively evaluated via a rules-based python script
- Shows great separation between models
- Difficulty can easily be adjusted with a single line change
- An evaluation costs less than $0.05 for most models
- Does not need a complicated evaluation harness or even an API to run
