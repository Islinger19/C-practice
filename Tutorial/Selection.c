#include <stdio.h>

int Selsort(){
    int min_index,n;
    int a[5]= {25,32,11,16,13};
    int swap;
    for (int i = 0; i < n-1; i++)
    {
        min_index=i;
        for (int j = 0; j < i+1; j++)
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
        printf("%d ",&a[i]);
    }
    return 0;
}

int main(){
    Selsort();
    return 0;
}
