use roxmltree::Document;
use std::collections::{HashSet, HashMap};
use std::fs;

// Function that calculates the Damerau-Levenshtein distance.
// This is a measure of the difference between two strings.
// It accounts for addition, deletion, substitution, and the transposition of two adjacent characters.
fn damerau_levenshtein(a: &str, b: &str) -> usize {
    // Convert the input strings to character arrays and get their lengths.
    let len_a = a.chars().count();
    let len_b = b.chars().count();

    // Initialize a two-dimensional vector to store the intermediate results of the calculation.
    // This vector has dimensions (len_a + 1) x (len_b + 1).
    let mut d = vec![vec![0; len_b + 1]; len_a + 1];

    // Initialize the first row and the first column of the vector.
    for i in 0..=len_a {
        d[i][0] = i;
    }
    for j in 0..=len_b {
        d[0][j] = j;
    }

    // Loop over both strings.
    for j in 1..=len_b {
        for i in 1..=len_a {
            // Compare each character from the first string with each character from the second string.
            // If the characters are the same, the cost of substitution is 0. Otherwise, it's 1.
            let cost = if a.chars().nth(i - 1).unwrap() == b.chars().nth(j - 1).unwrap() {
                0
            } else {
                1
            };

            // For each pair of characters, calculate the minimum cost between deletion, insertion,
            // substitution, or no operation.
            d[i][j] = std::cmp::min(
                std::cmp::min(d[i - 1][j] + 1, d[i][j - 1] + 1), // min(deletion, insertion)
                d[i - 1][j - 1] + cost, // substitution
            );

            // If we are beyond the first row and column, and transposition is possible (i.e., swapping
            // two letters would result in a match), then check if transposition results in a lower cost.
            // If so, update the cost.
            if i > 1 && j > 1
                && a.chars().nth(i - 1).unwrap() == b.chars().nth(j - 2).unwrap()
                && a.chars().nth(i - 2).unwrap() == b.chars().nth(j - 1).unwrap()
            {
                d[i][j] = std::cmp::min(d[i][j], d[i - 2][j - 2] + cost);
            }
        }
    }

    // The Damerau-Levenshtein distance is the value in the bottom right corner of the matrix.
    // This is the minimal cost of transforming one string into the other using deletions, insertions,
    // substitutions, and transpositions.
    d[len_a][len_b]
}

// This function takes a sentence as input and returns a vector of bigrams.
// A bigram is a pair of consecutive words.
fn get_bigrams(sentence: &str) -> Vec<(&str, &str)> {
    let words: Vec<_> = sentence.split_whitespace().collect();
    words.windows(2).map(|w| (w[0], w[1])).collect()
}

// This function takes a sentence and a set of bigrams as input.
// It returns the number of bigrams in the sentence that are either in the set or
// are a minor variation of a bigram in the set.
pub(crate) fn fuzzy_bigram_match(sentence: &str, bigram_set: &HashSet<(String, String)>) -> f32 {
    // Get the bigrams from the sentence.
    let sentence_bigrams = get_bigrams(sentence);
    // get the length of the sentence by splitting at whitespaces
    let sentence_length = sentence.split_whitespace().count();
    // Initialize a counter for the matches.
    let mut matches = 0;

    // For each bigram in the sentence, check if it's in the set or if it's a minor variation of a bigram in the set.
    for (word1, word2) in sentence_bigrams {
        if bigram_set.contains(&(word1.to_string(), word2.to_string())) {
            // The bigram is in the set, increment the counter.
            matches += 1;
        } else {
            // The bigram is not in the set, check for minor variations.
            for (set_word1, set_word2) in bigram_set.iter() {
                if damerau_levenshtein(word1, set_word1) <= 1 && damerau_levenshtein(word2, set_word2) <= 1 {
                    // The bigram is a minor variation of a bigram in the set, increment the counter.
                    matches += 1;
                    break;
                }
            }
        }
    }

    // calculate the propabiliy of the sentence being swiss german
    let probability = matches as f32 / sentence_length as f32;

    probability
}


// Function that receives the bigram set and returns a HashSet with all unique words
fn extract_unique_words(bigram_set: &HashSet<(String, String)>) -> HashSet<String> {
    let mut unique_words = HashSet::new();

    // Iterate over all bigrams
    for (word1, word2) in bigram_set.iter() {
        // Insert each word into the HashSet.
        // The insert operation does not insert duplicates, as it is a HashSet.
        unique_words.insert(word1.to_string());
        unique_words.insert(word2.to_string());
    }

    unique_words
}

pub(crate) fn bigrams_from_xml(xml: &str) -> HashSet<(String, String)> {
    let mut bigrams = HashSet::new();

    let doc = Document::parse(xml).unwrap();

    for article in doc.descendants().filter(|n| n.has_tag_name("article")) {
        for sentence in article.descendants().filter(|n| n.has_tag_name("s")) {
            let words: Vec<_> = sentence
                .descendants()
                .filter(|n| n.has_tag_name("w"))
                .filter_map(|n| n.text())
                .map(|s| s.to_owned())
                .collect();

            for bigram in words.windows(2) {
                bigrams.insert((bigram[0].clone(), bigram[1].clone()));
            }
        }
    }

    bigrams
}