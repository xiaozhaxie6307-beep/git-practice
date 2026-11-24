def two_sum_brute_force(numbers, target):
    for first in range(len(numbers)):
        for second in range(first + 1, len(numbers)):
            if numbers[first] + numbers[second] == target:
                return first, second
    return None


def two_sum(numbers, target):
    seen = {}
    for index, number in enumerate(numbers):
        needed = target - number
        if needed in seen:
            return seen[needed], index
        seen[number] = index
    return None


if __name__ == "__main__":
    for find_pair in (two_sum_brute_force, two_sum):
        assert find_pair([2, 7, 11, 15], 9) == (0, 1)
        assert find_pair([3, 3], 6) == (0, 1)
        assert find_pair([1, 2], 5) is None
        assert find_pair([], 5) is None
    print("两数之和检查通过。")