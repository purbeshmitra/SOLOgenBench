import sys
import json
import requests
import time
import os
from typing import List, Dict, Set, Tuple, Any

def read_word_list(filepath):
    """Read a word list file and return a set of words"""
    try:
        # Try with UTF-8 encoding first
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Fall back to latin-1 encoding which should handle most text files
        with open(filepath, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Check if the file is comma-separated or newline-separated
    if ',' in content:
        # Comma-separated format
        words = [word.strip().lower() for word in content.split(',')]
    else:
        # Newline-separated format
        words = [word.strip().lower() for word in content.splitlines() if word.strip()]
    
    return set(words)

def read_input_questions(filepath):
    """Read the input questions file and return a list of lines, handling numbered format"""
    try:
        # Try with UTF-8 encoding first
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except UnicodeDecodeError:
        # Fall back to latin-1 encoding which should handle most text files
        with open(filepath, 'r', encoding='latin-1') as f:
            lines = f.readlines()
    
    # Process lines to handle numbered format (e.g., "1. Can I win now?")
    processed_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if line starts with a number and period (e.g., "1.", "42.")
        import re
        match = re.match(r'^\d+\.\s*(.*)', line)
        if match:
            # Extract just the question part
            question = match.group(1).strip()
            if question:  # Skip empty questions
                processed_lines.append(question)
        elif line:  # Add non-empty lines that don't match the pattern
            processed_lines.append(line)
    
    return processed_lines

def clean_word(word):
    """Remove any punctuation from a word and convert to lowercase"""
    # Remove common punctuation that might appear at the end of words
    for char in '.,?!:;':
        word = word.replace(char, '')
    return word.lower()

def check_questions(questions, common_words, verbs, adjectives, nouns):
    """Check if questions meet all criteria"""
    results = []
    word_count = {}  # Track word usage across all questions
    already_used_words = set()  # Track words already used
    
    # Process each question
    for i, question in enumerate(questions, 1):
        words = question.split()
        cleaned_words = [clean_word(word) for word in words]
        cleaned_words = [word for word in cleaned_words if word]  # Remove empty strings
        
        # Check if question has exactly 4 words
        word_count_check = len(cleaned_words) == 4
        
        # Check if follows Verb + Adjective + Noun + Noun format
        format_check = False
        format_errors = []
        
        if word_count_check:
            # Check first word is a verb
            if cleaned_words[0] not in verbs:
                format_errors.append(f"First word '{cleaned_words[0]}' is not a verb")
            
            # Check second word is an adjective
            if cleaned_words[1] not in adjectives:
                format_errors.append(f"Second word '{cleaned_words[1]}' is not an adjective")
            
            # Check third word is a noun
            if cleaned_words[2] not in nouns:
                format_errors.append(f"Third word '{cleaned_words[2]}' is not a noun")
            
            # Check fourth word is a noun
            if cleaned_words[3] not in nouns:
                format_errors.append(f"Fourth word '{cleaned_words[3]}' is not a noun")
            
            # Format check passes if no errors
            format_check = len(format_errors) == 0
        
        # Find words not in common_words
        uncommon_words = [word for word in cleaned_words if word not in common_words]
        
        # Find words that have been used in previous questions
        previously_used_words = [word for word in cleaned_words if word in already_used_words]
        
        # Add current words to already_used_words for next questions
        already_used_words.update(cleaned_words)
        
        # Count all words for the summary
        for word in cleaned_words:
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1
        
        # Check if the question passes all criteria
        passes_common_check = len(uncommon_words) == 0
        passes_unique_check = len(previously_used_words) == 0
        passes_all = passes_common_check and passes_unique_check and word_count_check and format_check
        
        # Store results
        results.append({
            'question_num': i,
            'question': question,
            'uncommon_words': uncommon_words,
            'previously_used_words': previously_used_words,
            'word_count': len(cleaned_words),
            'word_count_check': word_count_check,
            'format_check': format_check,
            'format_errors': format_errors,
            'passes_all': passes_all
        })
    
    return results, word_count

def call_openrouter_api(prompt: str, api_key: str, model: str) -> Tuple[str, bool]:
    """
    Call the OpenRouter API with the given prompt and return the response.
    
    Args:
        prompt: The prompt to send to the API
        api_key: Your OpenRouter API key
        model: The model to use
        
    Returns:
        Tuple of (response_text, success_flag)
    """
    url = "https://openrouter.ai/api/v1/chat/completions"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Only include the required parameters
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 50000
    }
    
    try:
        print(f"Sending request to {url} for model {model}...")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        result = response.json()
        print(f"Response received with status code: {response.status_code}")
        
        # Print the structure of the response for debugging
        print("Response structure:")
        for key in result:
            print(f"  - {key}")
        
        # Check if 'choices' exists in the response
        if 'choices' not in result:
            print("ERROR: 'choices' field not found in the response")
            print(f"Full response: {json.dumps(result, indent=2)}")
            return f"ERROR: Model response format was unexpected. Full response: {json.dumps(result, indent=2)}", False
        
        if not result['choices'] or 'message' not in result['choices'][0]:
            print("ERROR: Expected message structure not found in choices")
            print(f"Choices content: {json.dumps(result['choices'], indent=2)}")
            return f"ERROR: Model response format was unexpected. Choices content: {json.dumps(result['choices'], indent=2)}", False
        
        return result['choices'][0]['message']['content'], True
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        error_msg = f"ERROR: API request failed: {str(e)}"
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response status code: {e.response.status_code}")
            print(f"Response text: {e.response.text}")
            error_msg += f"\nResponse status code: {e.response.status_code}\nResponse text: {e.response.text}"
        return error_msg, False
    except Exception as e:
        print(f"General error: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback_str = traceback.format_exc()
        print(traceback_str)
        return f"ERROR: An unexpected error occurred: {str(e)}\n{traceback_str}", False

def generate_llm_output(input_file: str, api_key: str, model: str) -> Tuple[List[str], str, bool]:
    """
    Read the entire prompt from file, send to LLM via OpenRouter, and extract responses
    
    Args:
        input_file: Path to input file containing the complete prompt
        api_key: OpenRouter API key
        model: Model to use
        
    Returns:
        Tuple of (list of extracted questions, raw response text, success flag)
    """
    # Read the input file as the complete prompt
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            prompt = f.read().strip()
    except UnicodeDecodeError:
        with open(input_file, 'r', encoding='latin-1') as f:
            prompt = f.read().strip()
            
    # Call the API with the exact content from the file
    print(f"Sending prompt to {model}...")
    response_text, success = call_openrouter_api(prompt, api_key, model)
    print("Response received.")
    
    # Process the response to extract the generated questions if successful
    questions = []
    if success:
        lines = response_text.strip().split('\n')
        
        # Extract numbered lines that look like responses
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # Look for lines that start with a number and period
            import re
            match = re.match(r'^\d+\.\s*(.*)', line)
            if match:
                question = match.group(1).strip()
                if question:  # Skip empty questions
                    questions.append(question)
    
    return questions, response_text, success

def get_safe_filename(model_name: str) -> str:
    """
    Convert a model name to a safe filename by replacing characters that
    would be problematic in filenames
    """
    # Replace slashes, colons, and other problematic characters
    return model_name.replace('/', '_').replace(':', '_').replace('\\', '_') \
                    .replace('*', '_').replace('?', '_').replace('"', '_') \
                    .replace('<', '_').replace('>', '_').replace('|', '_')

def main():
    # Default file names
    common_words_file = 'words.txt'
    SOLO_bench_input_file = 'SOLO_bench_Input.txt'
    verbs_file = 'verbs.txt'
    adjectives_file = 'adjectives.txt'
    nouns_file = 'nouns.txt'
    api_key_file = 'OpenRouterAPIKey.txt'
    
    # Default model
    default_model = "qwen/qwen3-30b-a3b:free"
    
    # Get OpenRouter API key from file
    try:
        with open(api_key_file, 'r') as f:
            api_key = f.read().strip()
        print(f"Successfully loaded API key from {api_key_file}")
    except FileNotFoundError:
        print(f"API key file {api_key_file} not found.")
        # Fall back to environment variable
        api_key = os.environ.get('OPENROUTER_API_KEY')
        if not api_key:
            api_key = input("Please enter your OpenRouter API key: ")
    except Exception as e:
        print(f"Error reading API key file: {e}")
        api_key = os.environ.get('OPENROUTER_API_KEY')
        if not api_key:
            api_key = input("Please enter your OpenRouter API key: ")
    
    # Allow command line arguments to specify files and model
    if len(sys.argv) > 1:
        # Check if the first argument is a model specification
        if sys.argv[1].startswith("--model="):
            model = sys.argv[1].split("=")[1]
            # Shift the arguments for files
            file_args_start = 2
        else:
            model = default_model
            file_args_start = 1
            
        # Process file arguments if present
        if len(sys.argv) > file_args_start:
            SOLO_bench_input_file = sys.argv[file_args_start]
        if len(sys.argv) > file_args_start + 1:
            common_words_file = sys.argv[file_args_start + 1]
        if len(sys.argv) > file_args_start + 2:
            verbs_file = sys.argv[file_args_start + 2]
        if len(sys.argv) > file_args_start + 3:
            adjectives_file = sys.argv[file_args_start + 3]
        if len(sys.argv) > file_args_start + 4:
            nouns_file = sys.argv[file_args_start + 4]
    else:
        model = default_model
    
    print(f"Using model: {model}")
    print(f"Reading common words from: {common_words_file}")
    print(f"Reading verbs from: {verbs_file}")
    print(f"Reading adjectives from: {adjectives_file}")
    print(f"Reading nouns from: {nouns_file}")
    print(f"Reading SOLO Bench prompt from: {SOLO_bench_input_file}")
    
    # Create a safe filename from the model name
    safe_model_name = get_safe_filename(model)
    timestamp = int(time.time())
    
    # Generate LLM output
    print(f"Generating responses from LLM ({model})...")
    questions, raw_response, success = generate_llm_output(SOLO_bench_input_file, api_key, model)
    
    # Always save the raw LLM output to file, even if there was an error
    raw_output_file = f"SOLO_bench_raw_{safe_model_name}_{timestamp}.txt"
    with open(raw_output_file, 'w', encoding='utf-8') as f:
        f.write(raw_response)
    print(f"Saved raw LLM output to {raw_output_file}")
    
    # If the API call failed, exit with error after saving the raw output
    if not success:
        print(f"ERROR: API call failed. Raw response has been saved to {raw_output_file}")
        # Optionally create a JSON summary file with the error
        error_results_file = f"SOLO_bench_{safe_model_name}_{timestamp}_error.json"
        error_data = {
            "model": model,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "status": "ERROR",
            "error_message": raw_response,
            "raw_output_file": raw_output_file
        }
        with open(error_results_file, 'w', encoding='utf-8') as f:
            json.dump(error_data, f, indent=2)
        print(f"Saved error summary to {error_results_file}")
        return
    
    print(f"Successfully generated {len(questions)} questions from LLM")
    
    # Save formatted questions to file
    output_file = f"SOLO_bench_{safe_model_name}_{timestamp}.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        for i, q in enumerate(questions, 1):
            f.write(f"{i}. {q}\n")
    print(f"Saved formatted LLM output to {output_file}")
    
    # Read files for validation
    try:
        common_words = read_word_list(common_words_file)
        print(f"Successfully loaded {len(common_words)} common words")
    except Exception as e:
        print(f"Error reading common words file: {e}")
        return
    
    try:
        verbs = read_word_list(verbs_file)
        print(f"Successfully loaded {len(verbs)} verbs")
    except Exception as e:
        print(f"Error reading verbs file: {e}")
        return
    
    try:
        adjectives = read_word_list(adjectives_file)
        print(f"Successfully loaded {len(adjectives)} adjectives")
    except Exception as e:
        print(f"Error reading adjectives file: {e}")
        return
    
    try:
        nouns = read_word_list(nouns_file)
        print(f"Successfully loaded {len(nouns)} nouns")
    except Exception as e:
        print(f"Error reading nouns file: {e}")
        return
    
    # Check questions
    results, word_count = check_questions(questions, common_words, verbs, adjectives, nouns)
    
    # Print results
    print("\nResults:")
    print("-" * 50)
    
    total_uncommon_words = 0
    unique_uncommon_words = set()
    
    for result in results:
        question_num = result['question_num']
        question = result['question']
        uncommon_words = result['uncommon_words']
        previously_used_words = result['previously_used_words']
        word_count_check = result['word_count_check']
        word_count_result = result['word_count']
        format_check = result['format_check']
        format_errors = result['format_errors']
        passes_all = result['passes_all']
        
        print(f"Question {question_num}: {question}")
        
        if not word_count_check:
            print(f"  Word count: {word_count_result} (should be exactly 4)")
        else:
            print(f"  Word count: {word_count_result} ✓")
        
        if not format_check:
            print(f"  Format check: Failed")
            for error in format_errors:
                print(f"    - {error}")
        else:
            print(f"  Format check: Verb + Adjective + Noun + Noun ✓")
        
        if uncommon_words:
            print(f"  Uncommon words: {', '.join(uncommon_words)}")
            total_uncommon_words += len(uncommon_words)
            unique_uncommon_words.update(uncommon_words)
        else:
            print("  All words are common ✓")
            
        if previously_used_words:
            print(f"  Previously used words: {', '.join(set(previously_used_words))}")
        else:
            print("  No words were used in previous questions ✓")
            
        print(f"  Overall status: {'PASSED' if passes_all else 'FAILED'}")
        print()
    
    # Summary
    print("Summary:")
    print("-" * 50)
    print(f"- Checked {len(questions)} questions from {model}")
    
    # Word count check summary
    questions_with_incorrect_word_count = sum(1 for r in results if not r['word_count_check'])
    print(f"- {questions_with_incorrect_word_count} questions did not have exactly 4 words")
    print(f"- {len(questions) - questions_with_incorrect_word_count} questions had exactly 4 words")
    
    # Format check summary
    questions_with_incorrect_format = sum(1 for r in results if not r['format_check'])
    print(f"- {questions_with_incorrect_format} questions did not follow the Verb + Adjective + Noun + Noun format")
    print(f"- {len(questions) - questions_with_incorrect_format} questions followed the correct format")
    
    # Common words check summary
    questions_with_uncommon = sum(1 for r in results if r['uncommon_words'])
    print(f"- {questions_with_uncommon} questions contained uncommon words")
    print(f"- {len(questions) - questions_with_uncommon} questions used only common words")
    print(f"- Found {total_uncommon_words} uncommon word occurrences in total")
    print(f"- Found {len(unique_uncommon_words)} unique uncommon words")
    
    # Previously used words check summary
    questions_with_previously_used = sum(1 for r in results if r['previously_used_words'])
    print(f"- {questions_with_previously_used} questions contained previously used words")
    print(f"- {len(questions) - questions_with_previously_used} questions used only new words")
    
    # Calculate and print overall score
    perfect_questions = sum(1 for r in results if r['passes_all'])
    score_percentage = (perfect_questions / len(questions) * 100) if questions else 0
    print("\nOverall Score:")
    print("-" * 50)
    print(f"Model: {model}")
    print(f"Score: {perfect_questions} out of {len(questions)} questions ({score_percentage:.1f}%) passed all criteria:")
    print("  1. Used exactly 4 words")
    print("  2. Followed the format: Verb + Adjective + Noun + Noun")
    print("  3. Used only words from the common words list")
    print("  4. Did not use any words that appeared in previous questions")
    
    # Save results to JSON file with model name in the filename
    results_file = f"SOLO_bench_{safe_model_name}_{timestamp}.json"
    result_data = {
        "model": model,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_questions": len(questions),
        "perfect_questions": perfect_questions,
        "score_percentage": score_percentage,
        "word_count_failures": questions_with_incorrect_word_count,
        "format_failures": questions_with_incorrect_format,
        "common_word_failures": questions_with_uncommon,
        "word_reuse_failures": questions_with_previously_used,
        "raw_output_file": raw_output_file,
        "formatted_output_file": output_file,
        "detailed_results": results
    }
    
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(result_data, f, indent=2)
    print(f"Saved detailed evaluation results to {results_file}")
    
    # List all repeated words with their counts
    words_used_multiple_times = {word: count for word, count in word_count.items() if count > 1}
    if words_used_multiple_times:
        print("\nWords used more than once across all questions:")
        for word in sorted(words_used_multiple_times.keys()):
            print(f"- '{word}' appears {words_used_multiple_times[word]} times")
    else:
        print("\nNo words were used more than once across all questions.")

if __name__ == "__main__":
    main()