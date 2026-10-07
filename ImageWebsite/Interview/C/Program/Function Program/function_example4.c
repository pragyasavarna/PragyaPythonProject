// Example 4: Argument Passed and Returns a Value
#include <stdio.h>
// Function Prototype
int addNumbers(int a, int b); 
int main() {
    int final_sum = addNumbers(30, 40); // Function Call with arguments
    printf("The returned sum is: %d\n", final_sum);
    return 0;
}
// Function Definition
int addNumbers(int a, int b) {
    int sum = a + b;
    return sum; // Returns the calculated sum
}