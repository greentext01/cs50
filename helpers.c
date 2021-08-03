#include "helpers.h"
#include <math.h>
#include <string.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            BYTE avg = (BYTE)round((image[y][x].rgbtRed + image[y][x].rgbtGreen + image[y][x].rgbtBlue) / 3.0);

            image[y][x].rgbtRed = avg;
            image[y][x].rgbtGreen = avg;
            image[y][x].rgbtBlue = avg;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width / 2; x++)
        {
            RGBTRIPLE tmp = image[y][width - x - 1];
            image[y][width - x - 1] = image[y][x];
            image[y][x] = tmp;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE originalImg[height][width];
    memcpy(originalImg, image, sizeof(RGBTRIPLE) * width * height);

    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            int totalRed = 0;
            int totalGreen = 0;
            int totalBlue = 0;
            int pixelAmount = 0;
            for (int cPixY = y - 1; cPixY <= y + 1; cPixY++)
            {
                for (int cPixX = x - 1; cPixX <= x + 1; cPixX++)
                {
                    if (cPixY >= 0 && cPixY < height && cPixX >= 0 && cPixX < width)
                    {
                        totalRed += originalImg[cPixY][cPixX].rgbtRed;
                        totalGreen += originalImg[cPixY][cPixX].rgbtGreen;
                        totalBlue += originalImg[cPixY][cPixX].rgbtBlue;
                        pixelAmount++;
                    }
                }
            }

            image[y][x].rgbtRed = totalRed / pixelAmount;
            image[y][x].rgbtGreen = totalGreen / pixelAmount;
            image[y][x].rgbtBlue = totalBlue / pixelAmount;
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    int matGX[3][3] = {
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1}};

    int matGY[3][3] = {
        {-1, -2, -1},
        {0, 0, 0},
        {1, 2, 1}};

    RGBTRIPLE originalImg[height][width];
    memcpy(originalImg, image, sizeof(RGBTRIPLE) * width * height);

    for (int y = 0; y < height; y++)
    {
        for (int x = 0; x < width; x++)
        {
            int totalRedX = 0;
            int totalGreenX = 0;
            int totalBlueX = 0;

            int totalRedY = 0;
            int totalGreenY = 0;
            int totalBlueY = 0;

            // For each neighboring pixel
            for (int cPixY = y - 1; cPixY <= y + 1; cPixY++)
            {
                for (int cPixX = x - 1; cPixX <= x + 1; cPixX++)
                {
                    // If pixel isn't past border
                    if (cPixY >= 0 && cPixY < height && cPixX >= 0 && cPixX < width)
                    {
                        // Gx for each channel
                        totalRedX += originalImg[cPixY][cPixX].rgbtRed * matGX[(cPixY - y) + 1][(cPixX - x) + 1];
                        totalGreenX += originalImg[cPixY][cPixX].rgbtGreen * matGX[(cPixY - y) + 1][(cPixX - x) + 1];
                        totalBlueX += originalImg[cPixY][cPixX].rgbtBlue * matGX[(cPixY - y) + 1][(cPixX - x) + 1];

                        // Gy
                        totalRedY += originalImg[cPixY][cPixX].rgbtRed * matGY[(cPixY - y) + 1][(cPixX - x) + 1];
                        totalGreenY += originalImg[cPixY][cPixX].rgbtGreen * matGY[(cPixY - y) + 1][(cPixX - x) + 1];
                        totalBlueY += originalImg[cPixY][cPixX].rgbtBlue * matGY[(cPixY - y) + 1][(cPixX - x) + 1];
                    }
                }
            }

            int redRes = (int)round(sqrt(pow(totalRedX, 2) + pow(totalRedY, 2)));
            int greenRes = (int)round(sqrt(pow(totalGreenX, 2) + pow(totalGreenY, 2)));
            int blueRes = (int)round(sqrt(pow(totalBlueX, 2) + pow(totalBlueY, 2)));

            image[y][x].rgbtRed = redRes > 255 ? 255 : redRes;
            image[y][x].rgbtGreen = greenRes > 255 ? 255 : greenRes;
            image[y][x].rgbtBlue = blueRes > 255 ? 255 : blueRes;
        }
    }
    return;
}
