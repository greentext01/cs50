// Implements a dictionary's functionality

#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
#include <ctype.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Number of buckets in hash table
const unsigned int N = 702;

// Hash table
node *table[N];

int wordCount = 0;

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    node *cursor = table[hash(word)];
    while (cursor)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    if (isalpha(word[0]))
    {
        if (strlen(word) > 1)
        {
            if (isalpha(word[1]))
            {
                return (tolower(word[0]) - 'a') * 27 + (tolower(word[1]) - 'a') + 1;
            }
        }

        return (tolower(word[0]) - 'a') * 27;
    }
    return 0;
}

void initBucket(char *word, node *n)
{
    strcpy(n->word, word);
    n->next = NULL;
    table[hash(word)] = n;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{

    FILE *file = fopen(dictionary, "r");

    if (!file)
    {
        return false;
    }

    char word[45];

    while (fscanf(file, "%s", word) != EOF)
    {
        wordCount++;
        node *n = malloc(sizeof(node));

        if (!n)
        {
            return false;
        }

        strcpy(n->word, word);

        if (!table[hash(word)])
        {
            initBucket(word, n);
        }
        else
        {
            n->next = table[hash(word)];
            table[hash(word)] = n;
        }
    }

    fclose(file);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    return wordCount;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }

    return true;
}
