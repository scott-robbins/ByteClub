#include <stdio.h>

__global__ void add (int*a, int*b, int*c) {
        *c = *a + *b;
}

void random_ints(int* arr, int n){
    int i;
    for (i = 0; i < n; ++i)
        arr[i] = rand();
}

#define N 512
int main(void){
    int *a, *b, *c;
    int *d_a, *d_b, *d_c;
    int size = N * sizeof(int);

    // Allocate space for device copies of a,b and c
    cudaMalloc((void **), &d_a, size);
    cudaMalloc((void **), &d_b, size);
    cudaMalloc((void **), &d_c, size);

    // Do the same for host copy space
    a = (int *)malloc(size);  random_ints(a, N);
    b = (int *)malloc(size);  random_ints(b, N);
    c = (int *)malloc(size);

    // Copy inputs to device
    cudaMemcpy(d_a, a, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_b, b, size, cudaMemcpyHostToDevice);
    cudaMemcpy(d_c, c, size, cudaMemcpyHostToDevice);

    // Launch add() kernel on GPU with N blocks
    add<<<N,1>>>(d_a, d_b, d_c);

    // Copy result back to host
    cudaMemcpy(c, d_c, size, cudaMemcpyHostToDevice);

    // Cleanup memory
    free(a); free(b); free(c);
    cudaFree(d_a); cudaFree(d_b); cudaFree(d_c);
    return 0;
}