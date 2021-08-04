#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>

bool isJpg(uint8_t *buffer);

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        puts("Usage: ./recover image");
        return 1;
    }
    uint8_t buffer[512];
    FILE *card = fopen(argv[1], "r");
    if (!card)
    {
        printf("%s could not be opened for reading.\n", argv[1]);
        return 1;
    }

    FILE *out = NULL;
    int jpgsRead = 0;
    while (fread(&buffer, 512, 1, card))
    {
        if (isJpg(buffer))
        {
            char filename[16];
            sprintf(filename, "%03i.jpg", jpgsRead);
            if (jpgsRead == 0)
            {
                out = fopen(filename, "w");
                fwrite(buffer, 512, 1, out);
            }
            else
            {
                fclose(out);
                out = fopen(filename, "w");
                fwrite(buffer, 512, 1, out);
            }
            jpgsRead++;
        }
        else
        {
            if (jpgsRead > 0)
            {
                fwrite(buffer, 512, 1, out);
            }
        }
    }

    if (out)
    {
        fclose(out);
    }

    fclose(card);

    return 0;
}

bool isJpg(uint8_t buffer[512])
{
    return buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0;
}