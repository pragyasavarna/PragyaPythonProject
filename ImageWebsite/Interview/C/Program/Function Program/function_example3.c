// Example 3: Argument Passed But No Return Value
#include <stdio.h>
// Function Prototype
void printSum(int a, int b); 
int main() {
    printSum(10, 20); // Function Call with arguments passed
    return 0;
}
// Function Definition
void printSum(int a, int b) {
    int sum = a + b;
    printf("The sum of %d and %d is: %d\n", a, b, sum);
    // No return statement needed for void
}