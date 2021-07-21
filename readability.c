#include <cs50.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include <math.h>

size_t count_letters(string str);
size_t count_words(string str);
size_t count_sentences(string str);

int main()
{
    // Prompt user
    string str = get_string("Text: ");

    // Get letters per 100 words
    double letPer100w = (double)count_letters(str) * 100 / (double)count_words(str);

    // Get sentences per 100 words
    double sentPer100w = (double)count_sentences(str) * 100 / (double)count_words(str);

    // Compute grade
    int grade = round(0.0588 * letPer100w - 0.296 * sentPer100w - 15.8);
    if (grade < 1)
    {
        printf("%s\n", "Before Grade 1");
    }
    else if (grade > 16)
    {
        printf("%s\n", "Grade 16+");
    }
    else
    {
        printf("Grade %i\n", grade);
    }
}

size_t count_letters(string str)
{
    size_t count = 0;
    for (size_t i = 0; i < strlen(str); i++)
    {
        // Adds to the count only if character is alphabetic
        if (isalpha(str[i]))
        {
            count++;
        }
    }

    return count;
}

size_t count_words(string str)
{
    // 1 word if string isn't empty
    int wCount = strcmp(str, "") != 0;
    for (size_t i = 0; i < strlen(str); i++)
    {
        if (str[i] == ' ')
        {
            wCount++;
        }
    }

    return (size_t)wCount;
}

size_t count_sentences(string str)
{
    size_t sCount = 0;
    for (size_t i = 0; i < strlen(str); i++)
    {
        // Adds to count only if character is punctuaion
        if (str[i] == '.' || str[i] == '?' || str[i] == '!')
        {
            sCount++;
        }
    }

    return sCount;
}
