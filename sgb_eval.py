import json
import re
from sgb_generation import NUM_SENTENCES_TO_GENERATE, GROUP_ORDER

def evaluate_llm_response(response_filename="sgb_response.txt", data_filename="sgb_word_data.json"):
    """
    Evaluates an LLM's response against the benchmark rules.
    
    Args:
        response_filename (str): The path to the file containing the LLM's output.
        data_filename (str): The path to the JSON file with the word-group map.
    """
    # --- Configuration (should match the generation script) ---
    EXPECTED_SENTENCES = NUM_SENTENCES_TO_GENERATE
    EXPECTED_WORDS_PER_SENTENCE = len(GROUP_ORDER)

    # --- Load necessary data ---
    try:
        with open(data_filename, 'r') as f:
            word_to_group_map = json.load(f)
    except FileNotFoundError:
        print(f"Error: Data file not found at '{data_filename}'. Please run the generation script first.")
        return

    try:
        with open(response_filename, 'r') as f:
            response_text = f.read()
    except FileNotFoundError:
        print(f"Error: Response file not found at '{response_filename}'. Please save the LLM output to this file.")
        return

    # --- Pre-process and parse the response ---
    # Normalize text to lowercase and split into lines
    lines = response_text.strip().lower().split('\n')
    
    # Clean up lines: remove numbering (e.g., "1. "), punctuation, and filter empty lines
    sentences = []
    for line in lines:
        cleaned_line = re.sub(r'^\d+\.\s*', '', line) # Remove "1. ", "2. ", etc.
        words = re.findall(r'\b[a-z]+\b', cleaned_line) # Find all word sequences
        if words:
            sentences.append(words)

    print("--- EVALUATION REPORT ---")
    print(f"Found {len(sentences)} potential sentences in the response.\n")
    
    # --- Evaluation ---
    all_words_used = []
    valid_sentences = 0
    errors = {
        "wrong_word_count": [],
        "hallucinated_word": [],
        "wrong_group_order": []
    }

    for i, s in enumerate(sentences, 1):
        is_valid = True
        
        # 1. Check for correct number of words
        if len(s) != EXPECTED_WORDS_PER_SENTENCE:
            errors["wrong_word_count"].append(f"Sentence {i}: Expected {EXPECTED_WORDS_PER_SENTENCE} words, but found {len(s)}. Line: '{' '.join(s)}'")
            is_valid = False
            continue

        # 2. Check for hallucinations and group order
        current_group_order = []
        for word in s:
            if word not in word_to_group_map:
                errors["hallucinated_word"].append(f"Sentence {i}: The word '{word}' is not in the provided word list.")
                is_valid = False
            else:
                current_group_order.append(word_to_group_map[word])
        
        if not is_valid: continue # Stop checking this sentence if words were hallucinated

        if current_group_order != GROUP_ORDER:
            errors["wrong_group_order"].append(f"Sentence {i}: Incorrect group order. Got {current_group_order}, expected {GROUP_ORDER}. Line: '{' '.join(s)}'")
            is_valid = False
        
        if is_valid:
            valid_sentences += 1
            all_words_used.extend(s)

    # 3. Check for word uniqueness across all valid sentences
    duplicate_words = []
    if len(all_words_used) != len(set(all_words_used)):
        seen = set()
        for word in all_words_used:
            if word in seen:
                duplicate_words.append(word)
            seen.add(word)

    # --- Print Results ---
    print(f"Total Valid Sentences: {valid_sentences} / {EXPECTED_SENTENCES}\n")

    if any(errors.values()):
        print("--- ERRORS FOUND ---")
        for error_type, messages in errors.items():
            if messages:
                print(f"\n>> {error_type.replace('_', ' ').title()} ({len(messages)}):")
                for msg in messages:
                    print(f"   - {msg}")
    
    if duplicate_words:
        print(f"\n>> Duplicate Words Found ({len(set(duplicate_words))} unique duplicates):")
        for word in sorted(list(set(duplicate_words))):
            print(f"   - The word '{word}' was used more than once.")

    print("\n--- FINAL SCORE ---")
    score = valid_sentences if not duplicate_words else 0
    if score < EXPECTED_SENTENCES or duplicate_words:
        print(f"Score: {score}/{EXPECTED_SENTENCES}. The response failed due to errors or duplicate words.")
    else:
        print(f"Score: {score}/{EXPECTED_SENTENCES}. PERFECT! All rules were followed.")
    print("------------------------")


if __name__ == "__main__":
    # To run this, make sure you have 'sgb_response.txt' and 'sgb_word_data.json'
    # in the same directory.
    evaluate_llm_response()