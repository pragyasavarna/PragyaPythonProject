#include <stdio.h>

int main() {
    // 1. Declare and assign three numbers directly
    int num1 = 10;
    int num2 = 15;
    int num3 = 22;

    // 2. Calculate the sum
    int sum = num1 + num2 + num3;

    // 3. Calculate the average
    float average = sum / 3;

    // 4. Print the results
    printf("Numbers: %d, %d, %d\n", num1, num2, num3);
    printf("Sum: %d\n", sum);
    printf("Average: %.2f\n", average);

    return 0;
}