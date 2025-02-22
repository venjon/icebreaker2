def add(a, b):
    return a + b

print(add(1, 2))

def fibonacci(n):
    # Handle base cases
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    
    # Calculate fibonacci using iteration
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b

# Example usage
print(fibonacci(10))  # Will print the 10th Fibonacci number (55)


