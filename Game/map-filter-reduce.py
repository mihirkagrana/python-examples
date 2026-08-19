import functools

mylist = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Step 1 - fiter even numbers
result_filter = list(filter(lambda x: x % 2 == 0, mylist))
print(result_filter)  # Output: [2, 4, 6, 8]

# Step 2 - square the filtered numbers
result_map = list(map(lambda x: x * 2, result_filter))
print(result_map)  # Output: [4, 8, 12, 16]

# Step 3 - sum the squared numbers
result_reduce = functools.reduce(lambda x, y: x + y, result_map)
print(result_reduce)  # Output: 40