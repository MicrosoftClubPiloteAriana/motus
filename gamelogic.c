#include <stdio.h>
#include <stdlib.h>

/*
	TODO: Task assigned to Hichem Zouaoui
*/

#define info(msg) printf("[i] %s\n", msg)

void init()
/**
 * Initializes words list.
 * This must be called once at the beginning of the program
 */
{
	info("Loading word list...");
	info("Done loading word list");
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
// Dummy for testing
	int* result = malloc(sizeof(int) * 5);
	result[0] = 0;
	result[1] = 2;
	result[2] = 2;
	result[3] = 0;
	result[4] = 1;
	return result;
}

void reset_word()
/**
 * Picks up a new word randomly.
 */
{
    info("A new word has been chosen");
}
