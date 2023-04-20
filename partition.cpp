#include <cstdio>
#include <cstdlib>
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <vector>
#include <time.h>
#include <math.h>
#include <cmath>
#include <ctime>
#include "maxheap.hpp"

#include <random>
#include <chrono>

using namespace std;

// HELPER METHODS

// generates a random sequence of 1, -1 as a random solution
std::vector<int> generateRandSol(int n) {

    std::vector<int> sol(n);

    for (int i = 0; i < n; i++) {
        int set = rand() & 1;
		sol[i] = (set != 1) ? -1 : 1;
    }

    return sol;

}

long residue(std::vector<long> nums, std::vector<int> sol, int n) 
{
    long res = 0;
    for (int i = 0; i < n; i++) 
    {
        res += sol[i] * nums[i];
    }
    return abs(res);
}


// HEURISTICS

// Karmarkar Karp's algorithm
long karmarkarKarp(MaxHeap h) {
    while (h.size() > 1) {
        long a = h.extractMax();
        long b = h.extractMax();
        h.insert(abs(a-b));
    }
    return h.extractMax();
}

// repeated random heuristic
long repeatedRandom(std::vector<long> testvec) {
    
    int n = testvec.size();

    std::vector<int> sol = generateRandSol(n);

    for (int i = 0; i < 25000; i++) {
        std::vector<int> sol2 = generateRandSol(n);
        if (residue(testvec, sol2, n) < residue(testvec, sol, n)) {
            sol = sol2;
        }
    }

    return residue(testvec, sol, n);

}

long hillClimbing(MaxHeap h) {

}

long simulatedAnnealing(MaxHeap h) {

}

void test() {

    MaxHeap test;
    std::vector<long> testvec;
    srand(time(0));

    for (int i = 0; i < 100; i++) {

        long range = 1000000000000LL; // set the range [1, 10^12]
        long randNum = rand() % range + 1;

        test.insert(randNum);
        testvec.push_back(randNum);

    }

    long n = karmarkarKarp(test);
    std::cout << n << std::endl;

}


int main(int argc, char* argv[]) {

    // test 

    // command line argument should be in form "./partition flag algorithm inputfile"
    /*if (argc != 4) {
        printf("Invalid arguments.");
        return 1;
    }*/

    test();

}