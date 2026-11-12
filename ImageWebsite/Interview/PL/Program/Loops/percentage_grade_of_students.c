#include <stdio.h>

int main() {
    float m1, m2, m3, m4, m5;
    float total, percentage;

    // 1. Ask the user to enter marks for 5 subjects
    printf("Enter marks for 5 subjects (out of 100): ");
    scanf("%f %f %f %f %f", &m1, &m2, &m3, &m4, &m5);

    // 2. Calculate the total and percentage
    total = m1 + m2 + m3 + m4 + m5;
    percentage = (total / 500.0) * 100.0; 

    // 3. Print the calculated percentage
    printf("Percentage: %.2f%%\n", percentage);

    // 4. Check the percentage and print the corresponding grade
    if (percentage >= 90.0) {
        printf("Grade: A\n");
    } else if (percentage >= 80.0) {
        printf("Grade: B\n");
    } else if (percentage >= 60.0) {
        printf("Grade: C\n");
    } else {
        printf("Grade: D\n");
    }

    return 0;
}