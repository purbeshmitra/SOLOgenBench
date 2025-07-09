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

1. Run `sgb_generation.py` to generate the prompt, which will be available at `sgb_input.txt`. 
2. This prompt contains instructions along with the generated word list and can be directly fed to LLM for generating a response. 
3. Copy and paste the LLM generated response to `sgb_response.txt`.
4. Run `sgb_eval.py` for getting the evaluation score.

### Note

There can be significant variation in scores from run-to-run. Ideally the benchmark would be evaluated as AVG@5 but I have not done that at this stage.

### Rankings at of July 8, 2025
**SOLOgenBench - 400 words of 5 letters each, 4 groups, 50 sentences**
| Model Name               | Score   |
|--------------------------|---------|
|GPT-4.1-mini | 20% |
|GPT-4.1 | 30% |
|GPT-4o | 30% |
|o3-mini | 100% |
|o4-mini | 56% |
|o3 | 100% |
|Claude-Sonnet-3.5 | 100% |
|Claude-Sonnet-3.7-thinking-32k | 100% |
|Claude-Sonnet-4 | 96% |
|Claude-Opus-4 | 96% |
|Gemini-2.5-flash-lite | 20% |
|Gemini-2.5-flash-lite-thinking | 96% |
|Gemini-2.5-flash | 100% |
|Gemini-2.5-flash-thinking | 100% |
|Gemini-2.5-pro | 100% |
|Grok-3-mini-beta | 58% |
|Grok-3-mini-high | 100% |
|Grok-3 | 82% |
|Grok-3-thinking | 96% |
|Llama-3.3-70B-instruct | 32% |
|Llama-4-scout-17b-16e-instruct | 20% |
|Llama-4-maverick-17b-128e-instruct | 76% |
|Deepseek-v3 | 32% |
|Deepseek-r1 | 64% |
|Qwen3-235B-A22B | 10% |
|Qwen3-235B-A22B | 40% |
|Mistral | 14% |
|Mistral-thinking | 74% |

### Some additional notes

* 400 words and 50 sentences were chosen because otherwise, they were not fitting the prompt size requirements of the models (except for Gemini).
* Only GPT-4o, Claude (in artifact), Gemini, Grok (in artifact), and Qwen models followed accurate response format. All other models responded with extra exlanation, like, "Sure, here are 50 sentences..." Responses from those outputs were manually extracted.
