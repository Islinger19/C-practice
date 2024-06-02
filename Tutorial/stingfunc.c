#include <stdio.h>

void stringOperations(char str[])
{
    int length = 0, charCount = 0, vowelCount = 0;
    char copyStr[100] = {"Sanidhya Awasthi"};

    while (str[length] != 0)
    {
        length++;
    }

    for (int i = 0; i < length; i++)
    {
        if ('A' <= str[i] && str[i] <= 'Z' || 'a' <= str[i] && str[i] <= 'z')
        {
            charCount++;
        }

        if (str[i] == 'a' || str[i] == 'e' || str[i] == 'i' || str[i] == 'o' || str[i] == 'u' ||
            str[i] == 'A' || str[i] == 'E' || str[i] == 'I' || str[i] == 'O' || str[i] == 'U')
        {
            vowelCount++;
        }
    }

    for (int i = 0; i < length; i++)
    {
        copyStr[i] = str[i];
    }
    copyStr[length] = '\0';

    printf("Length of the string: %d\n", length);
    printf("Total number of characters: %d\n", charCount);
    printf("Total number of vowels: %d\n", vowelCount);
    printf("Copied string: %s\n", copyStr);
}

int main()
{
    char str[100];

    printf("Enter a string: ");
    gets(str);

    stringOperations(str);

    return 0;
}