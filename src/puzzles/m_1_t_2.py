def remove_duplicates(nums: list[int]) -> int:
    hash_table = set()
    pointer = 0
    while pointer < len(nums):
        if nums[pointer] in hash_table:
            nums.pop(pointer)
        else:
            hash_table.add(nums[pointer])
            pointer += 1
    return len(nums), nums
