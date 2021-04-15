#include <cs50.h>
#include <stdio.h>

int main(void) {
  int start;
  int end;
  int i = 0;

  do {
    start = get_int("Start size: ");
  } while (start < 9);

  do {
    end = get_int("End size: ");
  } while (end < start);

  while (start < end) {
    i++;
    start += (start / 3 - start / 4);
  }

  printf("Years: %i\n", i);
}