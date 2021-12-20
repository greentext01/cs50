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

    // Verify key

    if (strlen(argv[1]) != 26)
    {
        puts("Key must contain 26 characters.");
        return 1;
    }

    for (size_t i = 0; i < 26; i++)
    {
        if (!isalpha(argv[1][i]))
        {
            puts("Key must be only alphabetic characters.");
            return 1;
        }

        for (size_t j = i + 1; j < strlen(argv[1]); j++)
        {
            if (argv[1][i] == argv[1][j])
            {
                puts("Key must be only unique characters.");
                return 1;
            }
        }
    }

    string plaintext = get_string("plaintext: ");

    printf("ciphertext: ");
    
    // Encrypt
    
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
