#include <stdio.h>

struct Rectangle {
    int length;
    int breadth;};
void init(struct Rectangle *R, int l, int b) {
    R->length = l;
    R->breadth = b;}
int area(struct Rectangle R) {
    return R.length * R.breadth;}
void changeLength(struct Rectangle *R, int l) {
    R->length = l;}
int main() {
    int A;
    struct Rectangle r;
    init(&r, 10, 5);
    printf("Initial length: %d\n", r.length);
    printf("Initial breadth: %d\n", r.breadth);
    A = area(r);
    printf("Area: %d\n", A);
    changeLength(&r, 20);
    printf("Modified length: %d\n", r.length);
    A = area(r);
    printf("New Area: %d\n", A);
    return 0;
}
