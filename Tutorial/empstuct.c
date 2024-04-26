#include <stdio.h>
struct Salary{
    float basic;
    float gross;
    float allowance;
    float tax;
};
struct Employee {
    int id;
    char name[50];
    char designation[50];
    char department[50];
    struct Salary BS;
};
void Calculate(struct Employee *e){
    e->BS.allowance=(0.2)*e->BS.basic;
    e->BS.tax=(0.1)*e->BS.basic;
    e->BS.gross=e->BS.basic+e->BS.allowance-e->BS.tax;
}
void Insert(struct Employee *e){
    printf("\nEnter ID: ");
    scanf("%d", &e->id);
    getchar();
    printf("\nEnter Name: ");
    scanf("%[^\n]s",e->name);
    getchar();
    printf("\nEnter Designation: ");
    scanf("%[^\n]s",e->designation);
    getchar();
    printf("\nEnter Department: ");
    scanf("%[^\n]s",e->department);
    getchar();
    printf("\nEnter Basic Salary: ");
    scanf("%f",&e->BS.basic);
    Calculate(e);
}
void Display(struct Employee e){
    printf("\n\
---------------------------------------------------------------------------------------------------------------------------\n\
    ID              Name            Designation            Gross           Basic            Allowance           Tax\n\
----------------------------------------------------------------------------------------------------------------------------\n\
    %d       %s        %s           %.2f        %.2f        %.2f        %.2f\n\n",\
e.id,e.name,e.designation,e.BS.gross,e.BS.basic,e.BS.allowance,e.BS.tax);
}
int main() {
    struct Employee emp;
    Insert(&emp);
    Display(emp);
    return 0;
}