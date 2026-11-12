#include <stdio.h>

int main() {
    int num;
    int count = 0;

    // 1. Ask the user for an integer
    printf("Enter an integer: ");
    scanf("%d", &num);

    // 2. Handle the special case where the user enters 0
    if (num == 0) {
        count = 1;
    }

    // 3. Count the digits using a while loop
    while (num != 0) {
        num = num / 10; // Remove the last digit
        count++;        // Increase the counter by 1
    }

    // 4. Print the final count
    printf("Total number of digits: %d\n", count);

    return 0;
}