#include <stdio.h>
#include <math.h>

int main() {
    float a, b, c, d, r1, r2;

    printf("Enter coefficients a, b, and c: ");
    scanf("%f %f %f", &a, &b, &c);

    d = b * b - 4 * a * c;

    switch (d > 0) {
        case 1:
            r1 = (-b + sqrt(d)) / (2 * a);
            r2 = (-b - sqrt(d)) / (2 * a);
            printf("Roots are real and different.\n");
            printf("Root 1 = %.2f\n", r1);
            printf("Root 2 = %.2f\n", r2);
            break;

        case 0:
            switch (d == 0) {
                case 1:
                    r1 = r2 = -b / (2 * a);
                    printf("Roots are real and same.\n");
                    printf("Root 1 = Root 2 = %.2f\n", r1);
                    break;

                case 0:
                    printf("Roots are complex and different.\n");
                    double realPart = -b / (2 * a);
                    double imaginaryPart = sqrt(-d) / (2 * a);
                    printf("Root 1 = %.2f + %.2fi\n", realPart, imaginaryPart);
                    printf("Root 2 = %.2f - %.2fi\n", realPart, imaginaryPart);
                    break;
            }
            break;
    }

    return 0;
}