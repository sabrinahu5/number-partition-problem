import sys
import random
from random import randint
import math
import heapq
import numpy as np
import matplotlib.pyplot as plt
import time

MAX_ITER = 25000

# HELPER FUNCTIONS

def generate_rand_sol(n):
    sol = []
    for i in range(n):
        random_choice = random.choice([-1,1])
        sol.append(random_choice)
    return sol

def calc_residues(nums, sol, n):
    sum = 0
    for i in range(n):
        sum += sol[i] * nums[i]
    return abs(sum)

def generate_neighbor(sol):
    n = len(sol)
    neighbor = sol.copy()
    rand_indices = random.sample(range(n),2)
    i = rand_indices[0]
    j = rand_indices[1]
    neighbor[i] = -neighbor[i]
    if random.random() < 0.5:
        neighbor[j] = -neighbor[j]
    return neighbor

def KK(nums):
    H = [-x for x in nums]
    heapq.heapify(H)
    while(len(H) > 1):
        x = heapq.heappop(H)
        y = heapq.heappop(H)
        heapq.heappush(H, x - y)
    return -heapq.heappop(H)

def RR(nums):
    n = len(nums)
    sol = generate_rand_sol(n)
    for _ in range(MAX_ITER):
        sol2 = generate_rand_sol(n)
        if calc_residues(nums, sol2, n) < calc_residues(nums, sol, n):
            sol = sol2.copy()
    #print("RR result:", calc_residues(nums, sol, n))
    return calc_residues(nums, sol, n)

def HC(nums):
    n = len(nums)
    sol = generate_rand_sol(n)
    for _ in range(MAX_ITER):
        sol2 = generate_neighbor(sol)
        if calc_residues(nums, sol2, n) < calc_residues(nums, sol, n):
            sol = sol2.copy()
    #print("HC result:", calc_residues(nums, sol, n))
    return calc_residues(nums, sol, n)

def T(iter):
    return pow(10, 10) * pow(.8, iter // 300)

def SA(nums):
    n = len(nums)
    sol = generate_rand_sol(n)
    sol3 = sol.copy()
    for i in range(MAX_ITER):
        sol2 = generate_neighbor(sol)
        if calc_residues(nums, sol2, n) < calc_residues(nums, sol, n):
            sol = sol2.copy()
        elif random.random() < pow(math.e, -(calc_residues(nums, sol2, n) - calc_residues(nums, sol, n))/T(i)):
            sol = sol2.copy()
        if calc_residues(nums, sol, n) < calc_residues(nums, sol3, n):
            sol3 = sol.copy()
    #print("SA result:", calc_residues(nums, sol3, n))
    return calc_residues(nums, sol3, n)

# PRE-PARTITIONING STUFF

def generate_partition(n):
    partition = []
    for i in range(n):
        rand_int = random.randint(0, n - 1)
        partition.append(rand_int)
    return partition

def p_generate_neighbor(sol):
    n = len(sol)
    neighbor = sol.copy()
    rand_indices = random.sample(range(n), 2)
    i = rand_indices[0]
    j = rand_indices[1]
    neighbor[i] = j
    return neighbor

def p_calc_residues(nums, partition, n):
    A_prime = [0] * (n)
    for i in range(n):
        A_prime[partition[i]] += nums[i]
    return KK(A_prime)

def p_RR(nums):
    n = len(nums)
    sol = generate_partition(n)
    for _ in range(MAX_ITER):
        sol2 = generate_partition(n)
        if p_calc_residues(nums, sol2, n) < p_calc_residues(nums, sol, n):
            sol = sol2.copy()
    return p_calc_residues(nums, sol, n)

def p_HC(nums):
    n = len(nums)
    sol = generate_partition(n)
    for _ in range(MAX_ITER):
        sol2 = p_generate_neighbor(sol)
        if p_calc_residues(nums, sol2, n) < p_calc_residues(nums, sol, n):
            sol = sol2.copy()
    return p_calc_residues(nums, sol, n)

def p_SA(nums):
    n = len(nums)
    sol = generate_partition(n)
    sol3 = sol.copy()
    for i in range(MAX_ITER):
        sol2 = p_generate_neighbor(sol)
        if p_calc_residues(nums, sol2, n) < p_calc_residues(nums, sol, n):
            sol = sol2.copy()
        elif random.random() < pow(math.e, -(p_calc_residues(nums, sol2, n) - p_calc_residues(nums, sol, n))/T(i)):
            sol = sol2.copy()
        if p_calc_residues(nums, sol, n) < p_calc_residues(nums, sol3, n):
            sol3 = sol.copy()
    return p_calc_residues(nums, sol3, n)



def main(args):

    if len(args) != 3:
        print("Not enough arguments.")
        return
    
    nums = []
    try:
        file = open(args[2], 'r')
        for num in file:
            nums.append(int(num))
        file.close()
    except:
        print("Error when reading input.")

    algorithm_type = int(args[1])
    match algorithm_type:
        case 0:
            print(KK(nums))
        case 1:
            print(RR(nums))
        case 2:
            print(HC(nums))
        case 3:
            print(SA(nums))
        case 11:
            print(p_RR(nums))
        case 12:
            print(p_HC(nums))
        case 13:
            print(p_SA(nums))
        


if __name__ == "__main__":
    main(sys.argv[1:])

    """
    kk_avg = 0
    kk_data = np.array([0]*50)
    for i in range(50):
        nums = np.array([randint(0, 10 ** 12) for _ in range(100)])
        start = time.perf_counter()
        kkval = KK(nums)
        end = time.perf_counter()
        elapsed = end - start
        kk_avg += elapsed
        kk_data[i] = elapsed

    print("KK time: ")
    print(kk_avg / 50)
    """
    """
    rr_avg = 0
    rr_data = np.array([0]*50)
    for i in range(50):
        nums = np.array([randint(0, 10 ** 12) for _ in range(100)])
        start = time.perf_counter()
        rrval = RR(nums)
        end = time.perf_counter()
        elapsed = end - start
        rr_avg += elapsed
        rr_data[i] = elapsed
    print("RR time: ")
    print(rr_avg / 50)

    hc_avg = 0
    hc_data = np.array([0]*50)
    for i in range(50):
        nums = np.array([randint(0, 10 ** 12) for _ in range(100)])
        start = time.perf_counter()
        hcval = HC(nums)
        end = time.perf_counter()
        elapsed = end - start
        hc_avg += elapsed
        hc_data[i] = elapsed
    print("HC time: ")
    print(hc_avg / 50)
    
    sa_avg = 0
    sa_data = np.array([0]*50)
    for i in range(50):
        nums = np.array([randint(0, 10 ** 12) for _ in range(100)])
        start = time.perf_counter()
        saval = SA(nums)
        end = time.perf_counter()
        elapsed = end - start
        sa_avg += elapsed
        sa_data[i] = elapsed
    print("SA time: ")
    print(sa_avg / 50)
    """
    """
    p_rr_avg = 0
    p_rr_data = np.array([0]*50)
    for i in range(50):
        nums = np.array([randint(0, 10 ** 12) for _ in range(100)])
        start = time.perf_counter()
        rrval = p_RR(nums)
        end = time.perf_counter()
        elapsed = end - start
        p_rr_avg += elapsed
        p_rr_data[i] = elapsed
    print("p_RR time: ")
    print(p_rr_avg / 50)

    p_hc_avg = 0
    p_hc_data = np.array([0]*50)
    for i in range(50):
        nums = np.array([randint(0, 10 ** 12) for _ in range(100)])
        start = time.perf_counter()
        hcval = p_HC(nums)
        end = time.perf_counter()
        elapsed = end - start
        p_hc_avg += elapsed
        p_hc_data[i] = elapsed
    print("p_HC time: ")
    print(p_hc_avg / 50)
    
    p_sa_avg = 0
    p_sa_data = np.array([0]*50)
    for i in range(50):
        nums = np.array([randint(0, 10 ** 12) for _ in range(100)])
        start = time.perf_counter()
        saval = p_SA(nums)
        end = time.perf_counter()
        elapsed = end - start
        p_sa_avg += elapsed
        p_sa_data[i] = elapsed
    print("p_SA time: ")
    print(p_sa_avg / 50)
    

    y5 = p_rr_data
    y6 = p_hc_data
    y7 = p_sa_data


    x = np.arange(1, 51)
    y1 = kk_data
    #y2 = rr_data
    #y3 = hc_data
    #y4 = sa_data

    plt.title("Comparison of Times for KK and Other Heuristics (in Sec)")
    plt.xlabel("Instance")
    plt.ylabel("Time Elapsed (seconds)")
    plt.plot(x, y1, label = "Karmarkar Karp")
    plt.plot(x, y5, label = "Repeated Random")
    plt.plot(x, y6, label = "Hill Climbing")
    plt.plot(x, y7, label = "Simulated Annealing")
    plt.legend()
    plt.show()
    """


