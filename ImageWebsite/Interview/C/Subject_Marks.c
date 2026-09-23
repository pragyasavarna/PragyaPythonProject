#include <stdio.h>
int main() {
    // 1. Declare and assign marks for 5 subjects directly
    int sub1 = 85;
    int sub2 = 90;
    int sub3 = 78;
    int sub4 = 92;
    int sub5 = 88;
    // 2. Calculate the total marks (out of 500)
    int total = sub1 + sub2 + sub3 + sub4 + sub5;
    // 3. Calculate the percentage using the full formula and float casting
    float percentage = ((float)total / 500) * 100;
    // 4. Print the results
    printf("Subject Marks: %d, %d, %d, %d, %d\n", sub1, sub2, sub3, sub4, sub5);
    printf("Total Marks: %d\n", total);
    printf("Percentage: %.2f%%\n", percentage);

    return 0;
}