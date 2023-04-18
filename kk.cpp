#include <cstdio>
#include <cstdlib>
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>
#include <time.h>
#include <math.h>
#include <cmath>
#include "maxheap.hpp"

#include <random>
#include <chrono>

using namespace std;

// implementation of Karmarkar-Karp algorithm
// given sequence of n nonneg integers, want to output n +- 1's to minimize the residue
// KK algorithm takes 2 largest elements in A and differencing them, replacing one with the difference and the other with 0




int main(int argc, char* argv[]) {

    // test 

    MaxHeap H;

    H.insert(1);
    H.insert(5);
    H.insert(12);
    H.insert(0);
    H.insert(2);
    long n = H.extractMax();
    std::cout << n << std::endl;
    long a = H.extractMax();
    std::cout << a << std::endl;




}