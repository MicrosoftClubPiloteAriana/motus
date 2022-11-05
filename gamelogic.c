#include <stdio.h>
#include <stdlib.h>

/*
	TODO: Task assigned to Hichem Zouaoui
*/

#define info(msg) printf("[i] %s\n", msg)

void init()
{
	info("Loading word list...");
	info("Done loading word list");
}


int* interpret(const char* word)
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
