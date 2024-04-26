#include <stdio.h>
#include <stdlib.h>

int main(){
    int n,*p;
    printf("\nPlease enter the size of the array: ");
    scanf("%d",&n);
    p=malloc(n*sizeof(int));
    printf("\nEnter the elements of the array:\n");
    for(int i=0;i<n;i++){
        scanf("%d",&p[i]);
    }
    printf("\nThe array is:\n");
    for(int i=0;i<n;i++){
        printf("%d ",p[i]);
    }
    printf("\n\n");
    free(p);
    return 0;
}