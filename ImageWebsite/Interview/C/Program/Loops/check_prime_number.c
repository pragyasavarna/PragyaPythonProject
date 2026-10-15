#include <stdio.h>

// A prime number is a whole number greater than 1 that has only two factors: 1 and itself
// A factor is a whole number that divides another number evenly, leaving no remainder.
// 1 * 100 = 100
// 2 * 50 = 100
// 4 * 25 = 100
// 5 * 20 = 100
// 10 * 10 = 100
int main() {
    int num;
    int isPrime = 1; // We start by assuming the number is prime (1 = true)

    // 1. Ask the user for a number
    printf("Enter a positive integer: ");
    scanf("%d", &num);

    // 2. Handle special cases: 0 and 1 are not prime numbers
    if (num == 0 || num == 1) {
        isPrime = 0; // Set to false
    } else {
        // 3. Check for factors from 2 up to half of the number
        for (int i = 2; i <= num / 2; i++) {
            if (num % i == 0) {
                isPrime = 0; // It divided perfectly, so it's not prime
                break;       // Stop checking further factors
            }
        }
    }

    // 4. Print the final result based on the flag
    if (isPrime == 1) {
        printf("%d is a prime number.\n", num);
    } else {
        printf("%d is not a prime number.\n", num);
    }

    return 0;
}