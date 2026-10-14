#include <stdio.h>

int main() {
    printf("Prime numbers from 1 to 50 are:\n");

    // Loop through numbers from 2 to 50 (since 1 is not a prime number)
    for (int i = 2; i <= 50; i++) {
        int isPrime = 1; // Assume the number is prime to start

        // Check if 'i' is divisible by any number from 2 up to half of 'i'
        for (int j = 2; j <= i / 2; j++) {
            if (i % j == 0) {
                isPrime = 0; // It divided perfectly, so it is not prime
                break;       // Stop checking further factors for this number
            }
        }

        // If the flag is still 1, the number is prime, so we print it
        if (isPrime == 1) {
            printf("%d ", i);
        }
    }

    printf("\n");
    return 0;
}