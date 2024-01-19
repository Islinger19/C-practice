#include <math.h>
#include <stdio.h>
int main() {
    double a, b, c, dis, r1, r2, rP, iP;
    printf("Enter coefficients a, b and c: ");
    scanf("%lf %lf %lf", &a, &b, &c);
    dis = b * b - 4 * a * c;
    
    if (dis > 0) {
        printf("Real roots unique");
        r1 = (-b + sqrt(dis)) / (2 * a);
        r2 = (-b - sqrt(dis)) / (2 * a);
        printf("root1 = %.2lf and root2 = %.2lf", r1, r2);
    }

    else if (dis == 0) {
        r1 = r2 = -b / (2 * a);
        printf("Real roots identical");
        printf("root1 = root2 = %.2lf;", r1);
    }

    else {
        rP = -b / (2 * a);
        iP = sqrt(-dis) / (2 * a);
        printf("Imaginary Roots");
        printf("root1 = %.2lf+%.2lfi and root2 = %.2lf-%.2lfi", rP, iP, rP, iP);
    }
    return 0;
}