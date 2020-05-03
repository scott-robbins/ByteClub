# CUDA - Compute Unified Device Architecture
I got an NVIDIA Jetson Nano, and I want to understand how to take advantage of the CUDA GPU. 
Using this part of the Repo as a place for my notes as I learn.
___________________________________________________________________________________________________________

Key Terms:
* Host    - the CPU
* Device  - the GPU

Code is written for both devices (unifying execution).

## Process Flow: 
1.Copy input data from CPU memory to GPU memory
2.Load GPU program and execute,caching data on chip for performance
3.Copy results from GPU memory to CPU memory

## Cuda Code Intro
Standard C Code for Host: 
```
# include <stdio.h>
int main(void){
    fprintf("Standard C Code\n");
}
```
NVIDA compiler nvcc can be used for compilation if theres no device code (GPU code) present. 
(This will also compile with gcc, because again it's *host* code.)
```
$ nvcc hi.cu
$ a.out
Hello World!
```

Let's rewrite the same example, but with device code.

```
# include <stdio.h>
__global__ void firstkernel (void) {

}

int main(void){
    firstkernel <<<1,1>>>();
    fprintf("Hello Device Code!\n");
    return 0; \\ Need to return values from GPU? This has no computation numerically
}
```

## Executing a function on the GPU

__global__ indicates that a function runs on the *device* and is called from *host code*. 

nvcc separates source code into host and device components. 
Device functions (e.g. firstkernel()) processed by NVIDIA compiler
Host functions (e.g. main()) processed by standard host compiler

Triple angle brackets mark a call from host-code to device-code (also called a “kernel launch”).


## Parallel Programming in CUDA C/C++
A simple kernel to add two integers:
```
__global__ void add (int*a, int*b, int*c) {
        *c = *a + *b;
}
```
add() runs on the device, so a, b and c must point to device memory.
This means we need to allocate memory on the GPU.

Device pointers point to GPU memory
* May be passed to/from host code
* May not be dereferenced in host code

Host pointers point to CPU memory
* May be passed to/from device codeMay not be dereferenced in device code
* Simple CUDA API for handling device memorycudaMalloc(), cudaFree(), cudaMemcpy()
* Similar to the C equivalents malloc(), free(), memcpy()


## Memory Management 
* Host and device memory are separate entities
* Device pointers point to GPU memory 
* May be passed to/from host code 
* May not be dereferenced in host code

Host pointers point to CPU memory
* May be passed to/from device code
* May not be de-referenced in device code

## Moving to Parallel
GPU computing is about massive parallelism
Run code in parallel on the device: 
*    add<<< 1, 1 >>>();
*    add<<< N, 1 >>>();

Now instead of executing the add() kernel once, we will execute it N times *in parallel*. 

Terminology: each parallel invocation of add() is referred to as a block
* The set of blocks is referred to as a grid
* Each invocation can refer to its block index using blockIdx.x
```
__global__ void add(int *a, int *b, int *c) {
        c[blockIdx.x] = a[blockIdx.x] + b[blockIdx.x];
}
```
By using blockIdx.xto index into the array, each block handles a different element of the array
```
__global__ voidadd(int*a, int*b, int*c) {
        c[blockIdx.x] = a[blockIdx.x] + b[blockIdx.x];
}
```

Now redesign main function running the add() kernel in parallel. 

[ CUDA Reference PDF](https://www.nvidia.com/docs/io/116711/sc11-cuda-c-basics.pdf)

###| LAST UPDATED *May 2020* |
