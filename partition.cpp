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

// calculates residue
long residue(std::vector<long> nums, std::vector<int> sol, int n) 
{
    long res = 0;
    for (int i = 0; i < n; i++) 
    {
        res += sol[i] * nums[i];
    }
    return abs(res);
}

// generates neighbor solution
std::vector<int> generateNeighbor(std::vector<int> sol) {

    int n = sol.size();

    std::vector<int> neighbor(n);

    int r = rand() % n;

	for (int i = 0; i < n; i++) 
    {
		neighbor[i] = sol[i];
	}

	
	neighbor[r] = -neighbor[r];

	int j = r;
	if ((double) rand() / RAND_MAX <= 0.5) {
		while (j == r) 
        {
			j = rand() % n;
		}
		neighbor[j] = -neighbor[j];
	}

	return neighbor;
}

// for simulated annealing
double cooling(int ITER) 
{
    return pow(10, 10) * pow(0.8, ITER / 300);
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

long hillClimbing(std::vector<long> testvec) {

    int n = testvec.size();

    std::vector<int> sol = generateRandSol(n);

    for (int i = 0; i < 25000; i++) {
        std::vector<int> sol2 = generateNeighbor(sol);
        if (residue(testvec, sol2, n) < residue(testvec, sol, n)) {
            sol = sol2;
        }
    }

    return residue(testvec, sol, n);

}

long simulatedAnnealing(std::vector<long> testvec) {

    int n = testvec.size();

    std::vector<int> sol = generateRandSol(n);
    std::vector<int> sol3 = sol;

    for (int i = 0; i < 25000; i++) {
        std::vector<int> sol2 = generateNeighbor(sol);

        long res2 = residue(testvec, sol2, n);
        long res1 = residue(testvec, sol, n);
        if (res2 < res1) {
            sol = sol2;
        } else if ((double) rand() / RAND_MAX < exp(- (long) (res2 - res1) / cooling(i))) {
            sol = sol2;
        }

        if (res1 < residue(testvec, sol3, n)) {
            sol3 = sol;
        }
    }

    return residue(testvec, sol3, n);

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
    std::cout << "Karmarkar Karp: " << n << std::endl;
    n = repeatedRandom(testvec);
    std::cout << "Repeated Random: " << n << std::endl;
    n = hillClimbing(testvec);
    std::cout << "Hill Climbing: " << n << std::endl;
    n = simulatedAnnealing(testvec);
    std::cout << "Simulated Annealing: " << n << std::endl;


}


int main(int argc, char* argv[]) {

    // test 

    // command line argument should be in form "./partition flag algorithm inputfile"
    if (argc != 4) {
        printf("Invalid arguments.");
        return 1;
    }

    test();

}