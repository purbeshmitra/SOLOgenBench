### What is it?

SOLO Bench is a benchmark that tasks LLMs to create 250 unique sentences, each exactly four words long in a specific grammatical format, using only words from a provided list of ~4,000 words. Each word from the list can only be used once across all sentences, and must be completed without external tools or code. This test aims to evaluate long-context (input and output) performance, memory, instruction following, reasoning, and hallucinations all in a single benchmark. It proves to be a very difficult task for all LLMs. The EASY version requests 250 sentences while MEDIUM requests 500. The benchmark gets signifcantly more difficult as the number of sentences requested increases. The HARD version is not needed yet...

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

### How to Use

The benchmark can be directly run by copying all the contents of SOLO_Bench_Input.txt into the prompt of any LLM. Paste the LLM output into eval.txt and run SOLO_Bench.py to evaluate its performance.

Alternatively you can use SOLO_Bench_OpenRouter.py to run and evaluate any model on OpenRouter. Note you will need an API key for non-free models. Use --model=modelname on the command line to specify a model. After completion it will generate a .txt with the raw LLM output and a .JSON file with the results of the benchmark. 

### Additional notes

There can be significant variation in scores from run-to-run. Ideally the benchmark would be evaluated as AVG@5 but I have not done that at this stage.

### Rankings at of 5/1/2025
**SOLO Bench - Easy**
| Model Name                                        | Score   |
|---------------------------------------------------|---------|
| gemini2.5-pro                                     | 74.80%  |
| o3                                               | 56.40%  |
| claude-3.7-sonnet:thinking                        | 34.00%  |
| grok-3-beta                                       | 31.20%  |
| deepseek-r1                                       | 28.40%  |
| gpt4.5                                           | 26.80%  |
| deepseek-chat-v3-0324                             | 20.00%  |
| gemini-2.5-flash-preview:thinking                 | 16.80%  |
| gpt-4.1                                          | 9.20%   |
| qwen3-235b-a22b                                   | 8.40%   |
| llama-3.1-nemotron-ultra-253b-v1:free             | 8.00%   |
| qwen3-32b:free                                    | 5.20%   |
| qwen2.5-vl-72b-instruct:free                      | 5.20%   |
| llama-4-maverick:free                             | 4.00%   |
| gemma-3-27b-it:free                               | 1.20%   |
| llama-3.3-70b-instruct                            | 0.40%   |
| gemma-3-4b-it:free                                | 0.00%   |
| qwen3-8b:free                                     | 0.00%   |
| llama-3.1-405b-instruct                           | 0.00%   |
| o4-mini-high*                                     | 0.00%   |
| llama-3.3-70b-instruct                            | 0.00%   |
| llama-4-scout                                     | 0.00%   |
* o4-mini-high refused to provide an answer

&nbsp;
&nbsp;

**SOLO Bench - Medium**
| Model Name                        | Score   |
|-----------------------------------|---------|
| gemini2.5-pro*                    | 57.80%  |
| claude-3.7-sonnet:thinking        | 13.60%  |
| deepseek-r1*                      | 11.80%  |
| o3*                               | 8.20%   |
| gpt4.5*                           | 5.80%   |
| grok-3-beta                       | 3.80%   |

* Models did not output all 500 sentences

