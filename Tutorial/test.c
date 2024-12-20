#include <stdio.h>
enum week
{
    Mon,
    Tue,
    Wed,
    Thur,
    Fri,
    Sat,
    Sun
};
void main()
{
    enum week day;
    day = Mon;
    printf("enum data: %d", day);
}