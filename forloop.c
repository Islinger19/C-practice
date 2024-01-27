
#include <stdio.h>

int main()
{
    int i = 0, j = 0; // Declare a variable 'i' to be used as the loop counter

    // The for loop starts with initialization, followed by the condition, and ends with the increment/decrement
    // In this example, the loop will execute as long as 'i' is less than or equal to 5 OR 'j' is less than 4
    // After each iteration, 'i' and 'j' will be incremented by 1
    // "||" is used as "or" in C "&&" for "and"
    // intialization; condition; increment/decrement
    // initialization is not compulsory is already initialized
    for (i = 0, j = 0; i <= 5, j < 12; )// only accepts last exp in exp 2
    {
        printf("%d  %d\n", i, j); // Print the current iteration number
        //exp 3 can be written here also
        i++; 
        j++;
    
    }


    return 0;
}
