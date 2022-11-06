#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <time.h>

#define WORD_LENGTH 5
#define COLOR_GRAY 0
#define COLOR_YELLOW 1
#define COLOR_GREEN 2

char* secret_word = NULL;

char* wordgen()
{
    FILE* fptr;
    fptr = fopen("words.txt", "r");

    srand(time(0));
    // generate a random number
    int c = rand() % 2305;
    printf("[i] Word index: %d\n", c);

    char* word = malloc(sizeof(char) * WORD_LENGTH);
    fseek(fptr, c * (WORD_LENGTH + 1), SEEK_SET);
    for (int i=0; i<WORD_LENGTH; i++) {
        // go to find the word letter by letter
        char c = fgetc(fptr);
        word[i] = c;
    }
    printf("[i] The word is %s\n", word);
    fclose(fptr);

    return word;
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
    memset(result, COLOR_GRAY, sizeof(result));
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
