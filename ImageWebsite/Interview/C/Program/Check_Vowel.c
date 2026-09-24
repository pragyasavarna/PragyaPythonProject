#include <stdio.h>

int main() {
    // 1. Declare and assign a character to test
    char ch = 'e'; 

    // 2. Check if the character is a lower or uppercase vowel
    if (ch == 'a' || ch == 'e' || ch == 'i' || ch == 'o' || ch == 'u' || 
        ch == 'A' || ch == 'E' || ch == 'I' || ch == 'O' || ch == 'U') {
        
        printf("%c is a vowel.\n", ch);
    } else {
        printf("%c is not a vowel.\n", ch);
    }

    return 0;
}