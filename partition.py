import sys
import random
from random import randint
import math
import heapq
import numpy as np
import matplotlib.pyplot as plt

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

def generate_tf():
    with open('input.txt', 'w') as f:
        for i in range(100):
            f.write(str(randint(0,10**12)))
            f.write('\n')

def call_algs(nums, alg):
    if alg == 0:
        return KK(nums)
    elif alg == 1:
        return RR(nums)
    elif alg == 2:
        return HC(nums)
    elif alg == 3:
        return SA(nums)
    elif alg == 11:
        return p_RR(nums)
    elif alg == 12:
        return p_HC(nums)
    elif alg == 13:
        return p_SA(nums)


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
        

"""
def run_algorithms(algorithms, data):
    results = []
    for A in data:
        instance_results = []
        for alg in algorithms:
            instance_results.append(call_algs(A, alg))
        results.append(instance_results)
    return results

def ranking_table(results):
    rankings = np.argsort(results, axis=1)
    counts = np.zeros((len(results[0]), len(results[0])), dtype=int)
    for rank in rankings:
        for i, alg_rank in enumerate(rank):
            counts[i][alg_rank] += 1
    return counts
"""

if __name__ == "__main__":
    main(sys.argv[1:])

    """
    kk_data = np.array([0]*50)
    for i in range(50):
        nums = np.array([randint(0, 10 ** 12) for _ in range(100)])
        kkval = KK(nums)
        kk_data[i] = kkval
    """

    """
    rr_data = np.array([0]*50)
    for i in range(50):
        nums = np.array([randint(0, 10 ** 12) for _ in range(100)])
        rrval = RR(nums)
        rr_data[i] = rrval

    hc_data = np.array([0]*50)
    for i in range(50):
        nums = np.array([randint(0, 10 ** 12) for _ in range(100)])
        hcval = HC(nums)
        hc_data[i] = hcval
    
    
    sa_data = np.array([0]*50)
    for i in range(50):
        nums = np.array([randint(0, 10 ** 12) for _ in range(100)])
        saval = SA(nums)
        sa_data[i] = saval

    """

    p_rr_data = np.array([0]*50)
    for i in range(50):
        nums = np.array([randint(0, 10 ** 12) for _ in range(100)])
        rrval = p_RR(nums)
        p_rr_data[i] = rrval

    p_hc_data = np.array([0]*50)
    for i in range(50):
        nums = np.array([randint(0, 10 ** 12) for _ in range(100)])
        hcval = p_HC(nums)
        p_hc_data[i] = hcval
    
    
    p_sa_data = np.array([0]*50)
    for i in range(50):
        nums = np.array([randint(0, 10 ** 12) for _ in range(100)])
        saval = p_SA(nums)
        p_sa_data[i] = saval

    y5 = p_rr_data
    y6 = p_hc_data
    y7 = p_sa_data


    x = np.arange(1, 51)
    #y1 = kk_data
    #y2 = rr_data
    #y3 = hc_data
    #y4 = sa_data

    plt.title("Comparison of Residues for KK and Pre-Partitioned Heuristics")
    plt.xlabel("Instance")
    plt.ylabel("Residues")
    #plt.plot(x, y1, label = "Karmarkar Karp")
    plt.plot(x, y5, label = "Repeated Random (P)")
    plt.plot(x, y6, label = "Hill Climbing (P)")
    plt.plot(x, y7, label = "Simulated Annealing (P)")
    plt.legend()
    plt.show()


    

"""
    # Generate 50 random instances of the problem
    num_instances = 1
    data = [np.array([randint(0, 10 ** 12) for _ in range(100)]) for _ in range(num_instances)]

    # List of algorithms
    algorithms = [0, 1, 2, 3, 11, 12, 13]
    algorithm_names = ["KK", "RR", "HC", "SA", "p_RR", "p_HC", "p_SA"]

    # Run all algorithms on the same data
    results = run_algorithms(algorithms, data)

    # Print s_residues table
    print("s_residues:")
    print("Instance\t", end="")
    for alg in algorithm_names:
        print(f"{alg}\t", end="")
    print()
    for i, instance_results in enumerate(results, start=1):
        print(f"{i}\t\t", end="")
        for res in instance_results:
            print(f"{res}\t", end="")
        print()

    # Print ranking table
    ranks = ranking_table(results)
    print("\nRankings:")
    print("Algorithm\t1st\t2nd\t3rd\t4th\t5th\t6th\t7th")

    for i, rank_counts in enumerate(ranks):
        print(f"{algorithm_names[i]}\t\t", end="")
        for count in rank_counts:
            print(f"{count}\t", end="")
        print()
"""