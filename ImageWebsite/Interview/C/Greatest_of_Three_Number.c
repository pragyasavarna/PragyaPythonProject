#include <stdio.h>

int main() {
    // 1. Declare and assign three numbers
    int num1 = 45;
    int num2 = 78;
    int num3 = 62;

    // 2. Use if-else statements to find the greatest
    if (num1 >= num2 && num1 >= num3) {
        printf("%d is the greatest.\n", num1);
    } else if (num2 >= num1 && num2 >= num3) {
        printf("%d is the greatest.\n", num2);
    } else {
        printf("%d is the greatest.\n", num3);
    }

    return 0;
}