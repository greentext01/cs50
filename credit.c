#include <cs50.h>
#include <stdio.h>
#define MAX 100

int main(void) {
  long cc_num;
  short cc_digits[MAX] = {};
  short cc_other_digits[MAX] = {};
  short cc_digits_not_mult[MAX] = {};
  int k;
  int i = 0;
  size_t cc_num_size;
  size_t cc_other_digits_size;
  bool is_valid;
  string cc_type;
  int multiplied_other_digits;

  cc_num = get_long("Enter your credit card number: ");

  do {
    k = cc_num % 10;
    cc_digits[i] = k;
    i++;
    cc_num /= 10;
  } while (cc_num != 0);

  cc_num_size = --i;
  i = 0;

  if (cc_digits[cc_num_size] == 4) {
    cc_type = "VISA";
  } else if (cc_digits[cc_num_size] == 3 &&
             (cc_digits[cc_num_size - 1] == 4 || cc_digits[cc_num_size - 1] == 7)) {
    cc_type = "AMEX";
  } else {
    cc_type = "MASTERCARD";
  }

  for (int j = cc_num_size; j > 0; j -= 2) {
    cc_other_digits[i] = cc_digits[j] * 2;
    i++;
  }
  cc_other_digits_size = --i;

  i = 0;

  for (int j = 0; j <= cc_other_digits_size; j++) {
    if (cc_other_digits[j] >= 10) {
      i += cc_other_digits[j] % 10;
      i += 1;
    } else {
      i += cc_other_digits[j];
    }
  }

  multiplied_other_digits = i;

  i = 0;

  for (int j = cc_num_size - 1; j >= 0; j -= 2) {
    cc_digits_not_mult[i] = cc_digits[j];
    i++;
  }

  for (int j = 0; j < i; j++) {
    multiplied_other_digits += cc_digits_not_mult[j];
  }

  if ((multiplied_other_digits % 10) != 0) {
    cc_type = "INVALID";
  }

  printf("%s\n", cc_type);
}