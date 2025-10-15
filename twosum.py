def two_sum(nums, target):
    lookup = {}
    for i, num in enumerate(nums):
        if target - num in lookup:
            return [lookup[target - num], i]
        lookup[num] = i

# Test
print(two_sum([2, 7, 11, 15], 9))  # Output: [0, 1]
