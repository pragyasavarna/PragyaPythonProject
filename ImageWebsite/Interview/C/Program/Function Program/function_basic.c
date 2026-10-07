#include <stdio.h>
/* 
Syntax of function prototype
returnType functionName(type1 argument1, type2 argument2, ...);
*/
int addNumbers(int a, int b);         // function prototype
int main()
{
    int n1,n2,sum,sum1;
    printf("Enters two numbers: ");
    scanf("%d %d",&n1,&n2);
    sum = addNumbers(n1, n2);        // function call
    sum1 = addNumbers(3, 5); 
    printf("sum = %d",sum);
    printf("sum = %d",sum1);
    return 0;
}
/* 
Syntax of function definition
returnType functionName(type1 argument1, type2 argument2, ...)
{
    //body of the function
}
*/
int addNumbers(int a, int b)         // function definition   
{
    int result;
    result = a+b;
    /*
    Syntax of return statement
    return (expression);
    */
    return result;                  // return statement
}