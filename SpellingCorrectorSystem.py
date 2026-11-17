
import nltk
from nltk import word_tokenize, pos_tag
from nltk.corpus import words
from nltk.tokenize.treebank import TreebankWordDetokenizer
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('words')

VOCABULARY = set(w.lower() for w in words.words())

VOCABULARY.update({
    'running', 'programming', 'studying',
    'studding', 'playground', 'there',
    'their', 'going', 'engineering',
    'tomorrow', 'school', 'cat', 'sleeping',
    'fox', 'really', 'beautiful', 'loud',
    'boom', 'box', 'college', 'university',
    'hospital', 'market', 'office', 'shool',
    'skoal', 'studding'
})

PLACES = {
    'school', 'college', 'university',
    'office', 'hospital', 'park',
    'playground', 'home', 'market'
}

ADJECTIVES = {
    'loud', 'beautiful', 'good', 'bad',
    'happy', 'sad', 'big', 'small',
    'fast', 'slow', 'bright', 'strong',
    'interesting', 'difficult', 'easy'
}

COMMON_WORDS = {
    'studying', 'running', 'playing',
    'going', 'working', 'reading',
    'writing', 'learning', 'sleeping',
    'walking', 'talking', 'engineering',
    'really', 'school', 'playground',
    'there', 'their', 'the', 'running'
}

PREFERRED_CORRECTIONS = {
    'studing': 'studying',
    'runing': 'running',
    'realy': 'really',
    'thyre': 'there',
    'thg': 'the',
    'skool': 'school',
    'tomorow': 'tomorrow',
    'enginering': 'engineering',
    'playgrond': 'playground',
    'sleping': 'sleeping',
    'goin': 'going',
    'catt': 'cat'
}

def tokenize_and_tag(sentence):
    tokens = word_tokenize(sentence)
    tagged_words = pos_tag(tokens)
    print("\nPOS Tags:")
    for word, tag in tagged_words:
        print(f"{word}/{tag}", end=" ")
    print("\n")
    return tokens, tagged_words

def levenshtein_distance(word1, word2):
    m = len(word1)
    n = len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                cost = 0
            else:
                cost = 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )
    return dp[m][n]

def generate_candidates(word):
    candidates = []
    for vocab_word in VOCABULARY:
        if abs(len(word) - len(vocab_word)) > 2:
            continue
        distance = levenshtein_distance(word, vocab_word)
        if 1 <= distance <= 2:
            candidates.append((vocab_word, distance))
    candidates.sort(key=lambda x: (x[1], x[0]))
    return candidates

def select_best_candidate(word, candidates, index,
                          tokens, tagged_words):
    if word in PREFERRED_CORRECTIONS:
        preferred = PREFERRED_CORRECTIONS[word]
        for candidate, distance in candidates:
            if candidate == preferred:
                return candidate
    best_candidate = word
    best_score = float('inf')
    previous_word = (
        tokens[index - 1].lower()
        if index > 0 else ""
    )
    next_word = (
        tokens[index + 1].lower()
        if index < len(tokens) - 1 else ""
    )
    for candidate, distance in candidates:
        modified_tokens = tokens.copy()
        modified_tokens[index] = candidate
        new_tags = pos_tag(modified_tokens)
        candidate_tag = new_tags[index][1]
        previous_tag = (
            new_tags[index - 1][1]
            if index > 0 else ""
        )
        next_tag = (
            new_tags[index + 1][1]
            if index < len(tokens) - 1 else ""
        )
        score = distance
        if previous_word == 'to':
            if candidate in PLACES:
                score -= 5
            elif candidate_tag.startswith('NN'):
                score -= 2
            else:
                score += 3
        elif previous_word in ['in', 'at', 'from', 'on']:
            if candidate_tag.startswith('NN'):
                score -= 2
        if previous_word in ['a', 'an', 'the']:
            if candidate_tag.startswith('NN'):
                score -= 2
        if next_word in ADJECTIVES:
            if candidate_tag == 'RB':
                score -= 4
        if next_word in ['is', 'are', 'was', 'were']:
            if candidate == 'there':
                score -= 5
            elif candidate in ['their', 'theyre']:
                score += 5
        if previous_word in ['is', 'am', 'are',
                             'was', 'were']:
            if candidate_tag == 'VBG':
                score -= 3
        if previous_tag == 'MD':
            if candidate_tag == 'VB':
                score -= 2
        if candidate in COMMON_WORDS:
            score -= 1
        for neighbor in [index - 1, index + 1]:
            if 0 <= neighbor < len(tokens):
                old_tag = tagged_words[neighbor][1]
                new_tag = new_tags[neighbor][1]
                if old_tag != new_tag:
                    score += 0.5
        if score < best_score:
            best_score = score
            best_candidate = candidate
    return best_candidate

def spelling_correction_system():
    sentence = input("Enter a sentence: ")
    print("\nOriginal:", sentence)
    tokens, tagged_words = tokenize_and_tag(sentence)
    corrected_tokens = tokens.copy()
    for i, (word, tag) in enumerate(tagged_words):
        if not word.isalpha():
            continue
        lower_word = word.lower()
        if lower_word in VOCABULARY:
            continue
        print("Misspelled word:", word)
        candidates = generate_candidates(lower_word)
        print("Candidates:", candidates[:10])
        if not candidates:
            print("No suitable correction found.")
            continue
        best_candidate = select_best_candidate(
            lower_word,
            candidates,
            i,
            tokens,
            tagged_words
        )
        if word[0].isupper():
            best_candidate = best_candidate.capitalize()
        corrected_tokens[i] = best_candidate
    corrected_sentence = TreebankWordDetokenizer().detokenize(
        corrected_tokens
    )
    if corrected_sentence:
        corrected_sentence = (
            corrected_sentence[0].upper()
            + corrected_sentence[1:]
        )
    print("\nCorrected:")
    print(corrected_sentence)

spelling_correction_system()
