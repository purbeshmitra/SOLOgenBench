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

def main():
    import sys
    
    # Default file names
    common_words_file = 'words.txt'
    input_file = 'eval.txt'
    verbs_file = 'verbs.txt'
    adjectives_file = 'adjectives.txt'
    nouns_file = 'nouns.txt'
    
    # Allow command line arguments to specify files
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    if len(sys.argv) > 2:
        common_words_file = sys.argv[2]
    if len(sys.argv) > 3:
        verbs_file = sys.argv[3]
    if len(sys.argv) > 4:
        adjectives_file = sys.argv[4]
    if len(sys.argv) > 5:
        nouns_file = sys.argv[5]
    
    print(f"Reading common words from: {common_words_file}")
    print(f"Reading verbs from: {verbs_file}")
    print(f"Reading adjectives from: {adjectives_file}")
    print(f"Reading nouns from: {nouns_file}")
    print(f"Reading questions from: {input_file}")
    
    # Read files
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
    
    try:
        questions = read_input_questions(input_file)
        print(f"Successfully loaded {len(questions)} questions")
    except Exception as e:
        print(f"Error reading input file: {e}")
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
    print(f"- Checked {len(questions)} questions")
    
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
    print("\nOverall Score:")
    print("-" * 50)
    print(f"- {perfect_questions} out of {len(questions)} questions ({perfect_questions/len(questions)*100:.1f}%) passed all criteria:")
    print("  1. Used exactly 4 words")
    print("  2. Followed the format: Verb + Adjective + Noun + Noun")
    print("  3. Used only words from the common words list")
    print("  4. Did not use any words that appeared in previous questions")
    
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