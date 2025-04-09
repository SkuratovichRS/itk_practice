def two_sum(nums: list[int], target: int) -> list[int]:
    pointer_1, pointer_2 = 0, 1
    while pointer_1 < len(nums):
        if pointer_2 >= len(nums):
            pointer_1 += 1
            pointer_2 = pointer_1 + 1
            if pointer_2 >= len(nums):
                return []
        sum_ = nums[pointer_1] + nums[pointer_2]
        if sum_ == target:
            return [pointer_1, pointer_2]
        pointer_2 += 1
    return []
