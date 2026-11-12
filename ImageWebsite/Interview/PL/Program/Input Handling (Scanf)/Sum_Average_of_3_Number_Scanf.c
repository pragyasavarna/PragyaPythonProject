#include <stdio.h>

int main() {
    // 1. Declare three numbers without assigning values
    int num1, num2, num3;

    // 2. Prompt the user and read the numbers using scanf
    printf("Enter three integers separated by spaces: ");
    scanf("%d %d %d", &num1, &num2, &num3);

    // 3. Calculate the sum
    int sum = num1 + num2 + num3;

    // 4. Calculate the average
    float average = (float)sum / 3;

    // 5. Print the results
    printf("Numbers: %d, %d, %d\n", num1, num2, num3);
    printf("Sum: %d\n", sum);
    printf("Average: %.2f\n", average);

    return 0;
}