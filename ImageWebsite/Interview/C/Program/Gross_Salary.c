#include <stdio.h>

int main() {
    // 1. Declare and assign the three salary components
    float basic = 25000.00;
    float da = 8000.501;   // Dearness Allowance
    float hra = 5000.80;  // House Rent Allowance

    // 2. Calculate the gross salary by adding them together
    float gross_salary = basic + da + hra;

    // 3. Print the individual components and the final gross salary
    printf("Basic Salary: %.2f\n", basic);
    printf("DA: %.2f\n", da);
    printf("HRA: %.2f\n", hra);
    printf("Gross Salary: %.2f\n", gross_salary);

    return 0;
}