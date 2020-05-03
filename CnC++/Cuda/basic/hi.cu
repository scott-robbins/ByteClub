#include <stdio.h>

__global__ void firstkernel (void) {
}

int main(void){
    firstkernel<<<1,1>>>();
    printf("Hello Device Code!\n");
    return 0;
}
