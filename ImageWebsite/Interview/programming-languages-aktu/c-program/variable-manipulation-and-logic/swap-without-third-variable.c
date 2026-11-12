
#include <stdio.h>

int main() {
    int a = 10;
    int b = 20;

    // Swap the numbers using addition and subtraction
    a = a + b;  // Step 1: 'a' becomes the sum of both (10 + 20 = 30)
    b = a - b;  // Step 2: 'b' becomes the original 'a' (30 - 20 = 10)
    a = a - b;  // Step 3: 'a' becomes the original 'b' (30 - 10 = 20)

    // Print only the final swapped result
    printf("After swap: a = %d, b = %d\n", a, b);

    return 0;
}