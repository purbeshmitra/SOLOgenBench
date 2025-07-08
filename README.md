### What is SOLOgenBench?

A generalized version of [SOLOBench](https://github.com/jd-3d/SOLOBench). It has the following additional features:

- More resilient to LLM training data contamination since each run generate new word list
- Uses made up words from random letters with proper group classification in context
- Prevents ambiguity of verb/noun/adjective classification of English words

### The following features of SOLOBench still applies to this version:

- MIT open-source license
- No single correct answer means it cannot be easily gamed or benchmaxxed
- Tests for medium context (10k tokens) input and output (2-8k tokens)
- Does not use LLM-as-a-judge or Human rating which is increasingly biased
- Is objectively evaluated via a rules-based python script
- Shows great separation between models
- Difficulty can easily be adjusted with a single line change
- An evaluation costs less than $0.05 for most models
- Does not need a complicated evaluation harness or even an API to run

### How to Use

1. Run sgb_generation.py to generate the prompt, which will be available at sgb_input.txt. 
2. This prompt contains instruction along with the generated word list and can be directly fed to the LLM for generating a response. 
3. Copy and paste the LLM generated response to sgb_response.txt.
4. Run sgb_eval.py for getting the evaluation score.

### Additional notes

There can be significant variation in scores from run-to-run. Ideally the benchmark would be evaluated as AVG@5 but I have not done that at this stage.