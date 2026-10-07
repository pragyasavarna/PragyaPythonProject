// Program Using continue in a For Loop
// The continue statement skips the current iteration of the loop and moves directly to the next one.
#include <stdio.h>
int main() {
    // Loop from 1 to 5
    for (int i = 1; i <= 5; i++) {
        // If i is 3, skip the print statement and continue to the next number
        if (i == 3) {
            continue; 
        }
        printf("%d\n", i);
    }
    printf("Loop finished.\n");
    return 0;
}