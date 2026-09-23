#include <stdio.h>

int main() {
    float length, width, area;

    // 1. Ask the user for the length and width
    printf("Enter the length of the rectangle: ");
    scanf("%f", &length);

    printf("Enter the width of the rectangle: ");
    scanf("%f", &width);

    // 2. Calculate the area (Length multiplied by Width)
    area = length * width;

    // 3. Print the result
    printf("Area of the rectangle: %.2f\n", area);

    return 0;
}