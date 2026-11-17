# POS-Based Spelling Correction System

An NLP-based spelling correction system that detects and corrects spelling errors in English sentences using **Levenshtein Edit Distance, Dynamic Programming, and Part-of-Speech (POS) Tagging**.

## Project Overview

Traditional spelling correction systems often select corrections solely based on minimum edit distance. However, multiple words can have similar spellings but different grammatical meanings.

This project aims to improve spelling correction by considering the grammatical role of words and their surrounding context while selecting the most appropriate correction.

The system accepts a sentence containing spelling errors, identifies potentially incorrect words, generates possible corrections, and selects suitable candidates using POS information and contextual rules.

## Features

- Sentence tokenization using NLTK.
- Part-of-Speech (POS) tagging for identifying grammatical roles.
- Levenshtein edit distance implemented using Dynamic Programming.
- Candidate word generation using a predefined English vocabulary.
- Identification of candidate words with edit distance 1 or 2.
- POS-based candidate selection.
- Contextual rules for improving spelling correction.
- Automatic reconstruction of the corrected sentence.

## Technologies Used

- Python
- NLTK (Natural Language Toolkit)
- Dynamic Programming
- Levenshtein Edit Distance
- POS Tagging

## How the System Works

The project is divided into four main tasks:

### 1. Sentence Tokenization and POS Tagging

The input sentence is tokenized into individual words using NLTK. Each token is assigned a Part-of-Speech tag to identify its grammatical category, such as noun, verb, adjective, or determiner.

### 2. Levenshtein Edit Distance

A Dynamic Programming approach is used to calculate the minimum number of operations required to transform one word into another.

The three operations considered are:

- Insertion
- Deletion
- Substitution

### 3. Candidate Word Generation

Each potentially misspelled word is compared against words in a predefined English vocabulary.

Words having an edit distance of 1 or 2 are considered possible correction candidates.

### 4. POS-Based Candidate Selection

Instead of selecting a correction based only on minimum edit distance, the system considers:

- POS compatibility.
- Grammatical structure.
- Surrounding words.
- Contextual correction rules.

The candidate with the most suitable combined score is selected.

## Example

**Input:**

```text
The boy is runing in the playgrond.
```

**POS Tags:**

```text
The/DT boy/NN is/VBZ runing/VBG
in/IN the/DT playgrond/NN
```

**Corrected Output:**

```text
The boy is running in the playground.
```

## Installation and Execution

### 1. Clone the Repository

```bash
git clone https://github.com/tanishkasirohi/POS-Based-Spelling-Correction.git
```

### 2. Navigate to the Project Directory

```bash
cd POS-Based-Spelling-Correction
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Program

```bash
python spelling_corrector.py
```

Enter a sentence containing spelling errors when prompted.

**Note:** An active internet connection is required during the first execution to download the necessary NLTK vocabulary and POS-tagging resources.

## Project Structure

```text
POS-Based-Spelling-Correction/
│
├── spelling_corrector.py
├── requirements.txt
└── README.md
```

## Complexity Analysis

- **Levenshtein Edit Distance:** O(m × n), where m and n are the lengths of the two words.
- **Candidate Generation:** O(V × m × n) in the worst case, where V is the vocabulary size.
- **Dynamic Programming Space Complexity:** O(m × n).

## Future Improvements

- Improve contextual understanding using language models.
- Expand vocabulary coverage.
- Improve correction of ambiguous words.
- Develop a graphical user interface.
- Support more complex grammatical structures.

## Author

**Tanishka Sirohi**

GitHub: [@tanishkasirohi](https://github.com/tanishkasirohi)

## Repository

[POS-Based-Spelling-Correction](https://github.com/tanishkasirohi/POS-Based-Spelling-Correction)
