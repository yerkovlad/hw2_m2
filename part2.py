import time
import multiprocessing

def factorize(number):
    def factorize_single(num):
        factors = []
        for i in range(1, num + 1):
            if num % i == 0:
                factors.append(i)
        return factors
    
    with multiprocessing.Pool() as pool:
        results = pool.map(factorize_single, number)
    
    return results

if __name__ == "__main__":
    numbers = [128, 255, 99999, 10651060]
    
    start_time = time.time()
    results = factorize(numbers)
    end_time = time.time()

    for i, factors in enumerate(results):
        print(f"Factors for {numbers[i]}: {factors}")

    print(f"Time taken: {end_time - start_time} seconds")
