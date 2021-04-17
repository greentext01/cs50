#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

string getNum(string prompt, int* size) {
  string out;
  bool is_valid;

  while (true) {
    is_valid = true;
    out = get_string("%s", prompt);
    *size = strlen(out);
    for (int i = 0; i < *size; i++) {
      if (!isdigit(out[i])) {
        is_valid = false;
      }

      out[i] -= 48;
    }

    if (is_valid) {
      return out;
    }
  }
}

bool checkValid(string cc_num, int cc_num_size) {
  if (cc_num_size > 19) {
    return 0;
  }
  char mult_digits[100];
  int total = 0;
  int j = 0;
  string cc_type;

  for (int i = cc_num_size - 2; i >= 0; i -= 2) {
    mult_digits[j] = cc_num[i] * 2;
    j++;
  }

  for (int i = 0; i < j; i++) {
    if (mult_digits[i] > 9) {
      total += 1;
    }
    total += mult_digits[i] % 10;
  }

  for (int i = cc_num_size - 1; i >= 0; i -= 2) {
    total += cc_num[i];
  }

  if (total % 10 != 0) {
    return false;
  } else {
    return true;
  }
}

bool checkMasterCard(string cc_num) {
  return cc_num[0] == 5 && (cc_num[1] == 1 || cc_num[1] == 2 ||
                            cc_num[1] == 3 || cc_num[1] == 4 || cc_num[1] == 5);
}

string check_cc_type(string cc_num, int cc_num_size) {
  if (!checkValid(cc_num, cc_num_size)) {
    return "INVALID";
  } else if (cc_num[0] == 4) {
    return "VISA";
  } else if (cc_num[0] == 3 && (cc_num[1] == 4 || cc_num[1] == 7)) {
    return "AMEX";
  } else if (checkMasterCard(cc_num)) {
    return "MASTERCARD";
  } else {
    return "INVALID";
  }
}

int main(void) {
  int size;
  string cc_num = getNum("Enter your credit card number: ", &size);
  printf("%s\n", check_cc_type(cc_num, size));
}