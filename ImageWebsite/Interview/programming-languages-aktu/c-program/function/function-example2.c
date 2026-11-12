// Example 2: No Arguments Passed But Returns a Value
#include <stdio.h>
// Function Prototype
int calculateSum(); 
int main() {
    int result = calculateSum(); // Function Call
    printf("The sum is: %d\n", result);
    return 0;
}
// Function Definition
int calculateSum() {
    int num1 = 15;
    int num2 = 25;
    int sum = num1 + num2;
    return sum; // Returns the sum of two numbers
}