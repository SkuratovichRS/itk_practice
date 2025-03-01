def binary_search(arr: list[int | float], numb: int | float) -> bool:
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (right + left) // 2
        if numb == arr[mid]:
            return True
        elif numb > arr[mid]:
            left = mid + 1
        else:
            right = mid - 1
    return False


arr = [1, 2, 3, 45, 356, 569, 600, 705, 923]
if __name__ == "__main__":
    assert binary_search(arr, 356)
    assert binary_search(arr, 1)
    assert binary_search(arr, 923)
    assert not binary_search(arr, 42)
