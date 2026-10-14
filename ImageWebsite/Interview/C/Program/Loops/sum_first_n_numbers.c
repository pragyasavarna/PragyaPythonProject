#include <stdio.h>

int main() {
    int n;
    int sum = 0;

    // 1. Ask the user for the value of N
    printf("Enter a positive integer: ");
    scanf("%d", &n);

    // 2. Add numbers from 1 up to N
    for (int i = 1; i <= n; i++) {
        sum = sum + i;
    }

    // 3. Print the final sum
    printf("Sum of the first %d natural numbers is: %d\n", n, sum);

    return 0;
}