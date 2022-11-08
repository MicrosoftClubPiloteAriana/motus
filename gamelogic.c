#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>

#define WORD_LENGTH 5
#define COLOR_GRAY 0
#define COLOR_YELLOW 1
#define COLOR_GREEN 2

#define WORDS_MAX 3000

char* secret_word = NULL;
char* words[WORDS_MAX];
int words_len;

void load_words()
{
    FILE* fptr = fopen("words.txt", "r");

    char* word = malloc(sizeof(char) * (WORD_LENGTH + 1));
    word[WORD_LENGTH] = '\0';

    int word_i = 0;
    int letter_i = 0;
    while(1) {
        // go to find the word letter by letter
        char c = fgetc(fptr);
        if (feof(fptr)) {
            break;
        }

        if (c == '\r' || c == '\n' || c == ' ' || c == '\t') {
            if (letter_i > 0)
            {
                letter_i = 0;
                words[word_i] = word;
                word_i++;
                word = malloc(sizeof(char) * (WORD_LENGTH + 1));
                word[WORD_LENGTH] = '\0';
            }
        } else {
            word[letter_i] = c;
            letter_i++;
        }
    }

    words_len = word_i;

    fclose(fptr);
}

char* wordgen()
{
    srand(time(0));
    int c = rand() % words_len;
    printf("[i] The word is %s at index %d\n", words[c], c);

    return words[c];
}

void reset_word()
/**
 * Picks up a new word randomly.
 */
{
    secret_word = wordgen();
}

void init()
/**
 * Initializes words list.
 * This must be called once at the beginning of the program
 */
{
    load_words();
    reset_word();
}


int* interpret(const char* word)
/**
 * Checks the try of the player.
 * @param const char* the word to check
 * @return An int array. Each value corresponds for a letter in order, it can be:
 *      - 0 -> the letter is not present at all
 *      - 1 -> the letter is present but not in the right location
 *      - 2 -> the letter is correct
 */
{
    bool forbidden_letters[WORD_LENGTH];
    memset(forbidden_letters, false, sizeof(forbidden_letters));
    int* result = malloc(sizeof(int) * WORD_LENGTH);
    memset(result, COLOR_GRAY, sizeof(int) * WORD_LENGTH);
    for (int i=0; i<WORD_LENGTH; i++) {
        if (secret_word[i] == word[i]){
            result[i] = COLOR_GREEN;
            forbidden_letters[i] = true;
        }
    }
    for (int r=0; r<WORD_LENGTH; r++) {
        if (result[r] == COLOR_GREEN) continue;
        for (int i=0; i<WORD_LENGTH; i++) {
            if (!forbidden_letters[i] && secret_word[i] == word[r]) {
                result[r] = COLOR_YELLOW;
                forbidden_letters[i] = true;
                break;
            }
        }
    }
    return result;
}

bool is_valid(const char* word)
{
    for (int i=0; i<words_len; i++) {
        if (strcmp(word, words[i]) == 0) return true;
    }
    return false;
}

char* get_secret_word()
{
    return secret_word;
}
