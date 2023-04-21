#include <cstdio>
#include <cstdlib>
#include <algorithm>
#include <cstdint>
#include <iostream>
#include <fstream>
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

// Karmarkar Karp's algorithm
long karmarkarKarp(std::vector<long> testvec) {

    MaxHeap h;
    for (int i = 0; i < testvec.size(); i++) {
        h.insert(testvec[i]);
    }

    while (h.size() > 1) {
        long a = h.extractMax();
        long b = h.extractMax();
        h.insert(abs(a-b));
    }
    return h.extractMax();
}

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
    for (int i = 0; i < n; i++) {
        res += sol[i] * nums[i];
    }
    return abs(res);
}

// generates neighbor solution
std::vector<int> generateNeighbor(std::vector<int> sol) {

    int n = sol.size();

    std::vector<int> neighbor(n);

    int r = rand() % n;

	for (int i = 0; i < n; i++) {
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

// generates a random prepartitioning )
std::vector<int> generatePartition(int n) {
    
    std::vector<int> partition(n);
    for (int i = 0; i < n; i++) 
    {
        partition[i] = rand() % n;
    }

    return partition;
}

// calculates residue but for prepartitioning
long residue_pre(std::vector<long> nums, std::vector<int> sol, int n) {
    std::vector<long> modified_sol(n);

    for (int i = 0; i < n; i++) {
        modified_sol[i] = 0;
    }

    for (int i = 0; i < n; i++) {
        modified_sol[sol[i]] += nums[i];
    }

    return karmarkarKarp(modified_sol);
}

std::vector<int> neighbor_pre(std::vector<int> sol) {

    int n = sol.size();

    std::vector<int> neighbor(n);

	for (int i = 0; i < n; i++) {
		neighbor[i] = sol[i];
	}

    int r = rand() % n;

	int j = neighbor[r];
	while (j == neighbor[r]) {
		j = rand() % n;
	}
	neighbor[r] = j;

	return neighbor;

}


// HEURISTICS


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

// hill climbing heuristic
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

// simulated annealing heuristic
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

std::vector<long> generateTest(){

    std::vector<long> testvec;
    srand(time(0));

    for (int i = 0; i < 100; i++) {

        long range = 1000000000000LL; // set the range [1, 10^12]
        long randNum = rand() % range + 1;

        testvec.push_back(randNum);
    }

    return testvec;

}

// repeated random heuristic w/ pre-partitioning
long rr_pre(std::vector<long> testvec) {
    
    int n = testvec.size();

    std::vector<int> sol = generatePartition(n);

    for (int i = 0; i < 25000; i++) {
        std::vector<int> sol2 = generateRandSol(n);
        if (residue_pre(testvec, sol2, n) < residue_pre(testvec, sol, n)) {
            sol = sol2;
        }
    }

    return residue_pre(testvec, sol, n);

}

void test() {

    long kk = 0;
    long rr = 0;
    long hc = 0;
    long sa = 0;
    long rrp = 0;

    for (int i = 0; i < 10; i++) {
        std::vector<long> testvec = generateTest();
        kk += karmarkarKarp(testvec);
        rr += repeatedRandom(testvec);
        hc += hillClimbing(testvec);
        sa += simulatedAnnealing(testvec);
        rrp += rr_pre(testvec);
    }

    std::cout << "Karmarkar Karp: " << kk / 10 << std::endl;
    std::cout << "Repeated Random: " << rr / 10 << std::endl;
    std::cout << "Hill Climbing: " << hc / 10 << std::endl;
    std::cout << "Simulated Annealing: " << sa / 10 << std::endl;
    std::cout << "Repeated Random with Pre-Partitioning: " << rrp / 10 << std::endl;


}


int main(int argc, char* argv[]) {

    // test 

    // command line argument should be in form "./partition flag algorithm inputfile"
    /*if (argc != 4) {
        printf("Usage: ./partition flag algorithm inputfile");
        return 0;
    }

    std::vector<long> testvec;
    if (atoi(argv[1]) == 0) {
        ifstream testfile(argv[3]);
        string line;
        while (getline(testfile, line)) {   
            testvec.push_back(stoi(line));
        }
    }


    if (atoi(argv[2]) == 0) {
        MaxHeap test;
        for (int i = 0; i < testvec.size(); i++) {
            test.insert(testvec[i]);
        }
        long n = karmarkarKarp(test);
        std::cout << n << std::endl;
    } else if (atoi(argv[2]) == 1) {
        long n = repeatedRandom(testvec);
        std::cout << n << std::endl;
    } else if (atoi(argv[2]) == 2) {
        long n = hillClimbing(testvec);
        std::cout << n << std::endl;
    } else if (atoi(argv[2]) == 3) {
        long n = simulatedAnnealing(testvec);
        std::cout << n << std::endl;
    }*/


    test();

    

}