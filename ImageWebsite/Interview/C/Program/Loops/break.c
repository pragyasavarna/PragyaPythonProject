// Program Using break in a For Loop
// The break statement completely stops and exits the loop as soon as the condition is met.
#include <stdio.h>

int main() {
    // Loop from 1 to 5
    for (int i = 1; i <= 5; i++) {
        // If i becomes 3, exit the loop entirely
        if (i == 4) {
            break; 
        }
        printf("%d\n", i);
    }
    printf("Loop exited.\n");
    return 0;
}