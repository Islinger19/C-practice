int main()
{
    int a, n = 1;
    printf("Enter number a : ");
    scanf("%d", &a);

    // printf("%d X 1 = %d\n", a , a*1);
    // printf("%d X 2 = %d\n", a , a*2);
    // printf("%d X 3 = %d\n", a , a*3);
    // printf("%d X 4 = %d\n", a , a*4);
    // printf("%d X 5 = %d\n", a , a*5);
    // printf("%d X 6 = %d\n", a , a*6);
    // printf("%d X 7 = %d\n", a , a*7);
    // printf("%d X 8 = %d\n", a , a*8);
    // printf("%d X 9 = %d\n", a , a*9);
    // printf("%d X 10 = %d\n", a , a*10);
    while (n <= 10)
    {
        printf("%d X %d = %d\n", a, n, a * n);
        n++;
    }
    return 0;
}
