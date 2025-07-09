import random
import string
import json

# --- Configuration ---
NUM_WORDS = 400
WORD_LENGTH = 5
NUM_GROUPS = 4
GROUP_ORDER = [4, 1, 3, 2]
NUM_SENTENCES_TO_GENERATE = 50

def generate_word_list_and_prompt():
    """
    Generates a list of 400 unique 7-letter words, assigns each to a
    random group (1-4), and creates a formatted prompt for an LLM.

    Saves the word-group data to 'sgb_word_data.json' for later evaluation.
    """

    # --- Generate unique words ---
    print("Generating unique word list...")
    unique_words = set()
    while len(unique_words) < NUM_WORDS:
        word = ''.join(random.choice(string.ascii_lowercase) for _ in range(WORD_LENGTH))
        unique_words.add(word)
    
    word_list = sorted(list(unique_words))

    # --- Assign words to groups ---
    word_to_group_map = {word: random.randint(1, NUM_GROUPS) for word in word_list}

    # Save the word-group map for the evaluation script
    with open('sgb_word_data.json', 'w') as f:
        json.dump(word_to_group_map, f, indent=4)
    print("Successfully saved word-to-group mapping to 'sgb_word_data.json'")

    # --- Construct the prompt ---
    prompt_header = f"""### TASK ###
You must generate exactly {NUM_SENTENCES_TO_GENERATE} unique four-word sentences.

### RULES ###
1.  **Uniqueness**: EVERY word you use across ALL {NUM_SENTENCES_TO_GENERATE} sentences must be unique. No word can be repeated.
2.  **Word Source**: You can ONLY use words from the "Word List" provided below. Do not use any other words.
3.  **Sentence Structure**: Each sentence must contain exactly four words.
4.  **Group Order**: The words in each sentence must follow a specific group order. The first word must be from Group {GROUP_ORDER[0]}, the second from Group {GROUP_ORDER[1]}, the third from Group {GROUP_ORDER[2]}, and the fourth from Group {GROUP_ORDER[3]}.
5.  **Output Format**: Present your answer as a numbered list of {NUM_SENTENCES_TO_GENERATE} sentences. Do not include group numbers or any other explanations in your final output.
6.  **No Tool Usage**: Do not use any tools or code to accomplish the task.

### WORD LIST ###
The list below contains {NUM_WORDS} words. Each word is followed by its group number in parentheses, like "word (Group X)". You must use this list to form your sentences according to the rules above.
---
"""

    # Format the word list for the prompt
    formatted_word_list = []
    for word, group in word_to_group_map.items():
        formatted_word_list.append(f"{word} (Group {group})")

    full_prompt = prompt_header + "\n".join(formatted_word_list)

    # Save the full prompt to a file
    with open('sgb_input.txt', 'w') as f:
        f.write(full_prompt)
    print("\nSuccessfully generated and saved prompt to 'input.txt'")
    print(f"\nTask configured with group order: {GROUP_ORDER}")

    # This script creates an empty file named "sgb_response.txt".
    # If the file already exists, this will overwrite it with a new empty file.

    file_name = "sgb_response.txt"

    try:
        with open(file_name, 'w') as f:
            # Opening the file in 'w' (write) mode and immediately closing it
            # is enough to create an empty file.
            pass 
        print(f"Successfully created empty file: {file_name}")
    except IOError as e:
        print(f"Error creating file: {e}")


if __name__ == "__main__":
    generate_word_list_and_prompt()
