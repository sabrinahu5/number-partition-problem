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

long kk(MaxHeap h) {
    while (h.size() > 1) {
        long a = h.extractMax();
        long b = h.extractMax();
        h.insert(abs(a-b));
    }
    return h.extractMax();
}




int main(int argc, char* argv[]) {

    // test 

    // command line argument should be in form "./partition flag algorithm inputfile"
    /*if (argc != 4) {
        printf("Invalid arguments.");
        return 1;
    }*/

    MaxHeap H;

    H.insert(7);
    H.insert(5);
    H.insert(10);
    H.insert(8);
    H.insert(6);
    long n = kk(H);
    std::cout << n << std::endl;




}