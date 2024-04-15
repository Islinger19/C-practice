#include <stdio.h>

void Selsort(int a[5]){
    int min_index, n=5;
    int swap;
    for (int i = 0; i < n-1; i++)
    {
        min_index=i;
        for (int j = i+1; j < n; j++) 
        {
            if (a[j]<a[min_index])
            {
                min_index=j;
            }
        }
        if (i != min_index)
        {
            swap=a[i];
            a[i]=a[min_index];
            a[min_index]=swap;
        }
                
    }
    for(int i=0;i<5;i++){
        printf("%d ", a[i]); 
    }
}

int main(){
    int a[5]= {25,32,11,16,13};
    Selsort(a); 
    return 0;
}
