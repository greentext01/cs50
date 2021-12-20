#include <cs50.h>
#include <string.h>
#include <stdio.h>
#include <ctype.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        puts("Usage: ./substitution key");
        return 1;
    }

    if (strlen(argv[1]) != 26)
    {
        puts("Key must contain 26 characters.");
        return 1;
    }

    string plaintext = get_string("plaintext: ");
    printf("ciphertext: ");
    for (size_t i = 0; i < strlen(plaintext); i++)
    {
        if (isalpha(plaintext[i]))
        {
            if (isupper(plaintext[i]))
            {
                printf("%c", toupper(argv[1][plaintext[i] - 'A']));
            }
            else
            {
                printf("%c", tolower(argv[1][plaintext[i] - 'a']));
            }
        }
        else
        {
            printf("%c", plaintext[i]);
        }
    }
    puts("");

    return 0;
}
