#include <stdio.h>

int main() {
    int n;

    // 1. Ask the user for the number
    printf("Enter a number: ");
    scanf("%d", &n);

    printf("Multiplication Table of %d:\n", n);

    // 2. Loop from 1 to 10 to calculate and print the table
    for (int i = 1; i <= 10; i++) {
        printf("%d x %d = %d\n", n, i, n * i);
    }

    return 0;
}