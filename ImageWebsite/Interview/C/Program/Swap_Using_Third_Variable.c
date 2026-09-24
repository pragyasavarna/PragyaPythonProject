
#include <stdio.h>

int main() {
    // 1. Declare two numbers and a third variable (temp)
    int a = 10;
    int b = 20;
    int temp; 

    // 2. Swap the numbers using 'temp'
    temp = a;  // 10 Step 1: Save the value of 'a' safely in 'temp'
    a = b;     // 20 Step 2: Copy the value of 'b' into 'a'
    b = temp;  // 10 Step 3: Put the saved value from 'temp' into 'b'

    // 3. Print only the final swapped result
    printf("After swap: a = %d, b = %d", a, b);

    return 0;
}