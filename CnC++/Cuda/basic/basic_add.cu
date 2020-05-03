#include <stdio.h>

__global__ void add (int*a, int*b, int*c) {
        *c = *a + *b;
}

int main(void){
    int a, b, c;
    int *d_a, *d_b, *d_c;
    int size = sizeof(int);

    // Make space for device copies of vars
    cudaMalloc((void**)&d_a, size);
    cudaMalloc((void**)&d_b, size);
    cudaMalloc((void**)&d_c, size);

    a = 2;
    b = 7;

    // Copy inputs to device
    cudaMemcpy(d_a, &a, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, &b, size, cudaMemcpyHostToDevice);

    // Launch add() kernel on GPU
    add<<<1,1>>>(d_a, d_b, d_c);// Copy result back to host
    cudaMemcpy(&c, d_c, size, cudaMemcpyDeviceToHost);

    cudaFree(d_a); cudaFree(d_b); cudaFree(d_c);

    // show the result
    printf("Result: %d\n", c);
    return 0;
}