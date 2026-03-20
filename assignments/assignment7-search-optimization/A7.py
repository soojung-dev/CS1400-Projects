# A7.py
# Assignment 7: Search & Loop Patterns + Performance Measurement
# Written by Soojung Kim
#
# NOTE: Do not use min(), max(), 'in' for membership tests, list.index(), count(),
# set(), join(), or str(list) to solve required logic.
# We implement loop patterns explicitly as taught in class.
#
# Each function includes:
# - optimization loops (find best)
# - accumulator loops (build new list / string)
# - sequential search
# - binary search
#
# main() contains tests:
# For every function (except measure_search_times), we print:
#   what we're testing
#   expected result
#   actual result
# with multiple tests including edge cases.

import random
import time


def curve_scores(scores):
    """
    curve_scores(scores: list[int]) -> list[int]

    Return a NEW list where:
    - the highest score in 'scores' is curved up to 100
    - every other score is increased by the same amount
    - order is preserved
    If 'scores' is empty, return [].

    This is solved in two steps:
    (1) Optimization loop: manually find the maximum score
    (2) Accumulator loop: build a new curved list by adding (100 - max_score)
    """
    # Step 0: empty → empty
    if len(scores) == 0:
        return []

    # Step 1: optimization loop to find max (no max() allowed)
    best = scores[0]
    for i in range(1, len(scores)):
        if scores[i] > best:
            best = scores[i]

    # Step 2: accumulator loop to build curved list
    shift = 100 - best
    curved_list = []
    for value in scores:
        curved_list.append(value + shift)

    return curved_list


def contains_duplicate(words):
    """
    contains_duplicate(words: list[str]) -> bool

    Return True if any string appears 2 or more times in the list,
    otherwise return False.

    Works for lists of any length, including 0 or 1.

    Strategy (sequential search idea):
    - For each index i, look at words[i]
    - Then scan the rest of the list (i+1 .. end)
      If we ever see the same word again, return True
    - If we finish with no match, return False
    """
    n = len(words)
    for i in range(n):
        current_word = words[i]
        # Search for another copy of current_word later in the list
        for j in range(i + 1, n):
            if words[j] == current_word:
                return True
    return False


def list_to_string(nums):
    """
    list_to_string(nums: list[int]) -> str

    Return a string that looks exactly like Python would print the list,
    e.g. [1, 2, 3] or [].

    We are NOT allowed to just do str(nums) or ", ".join(...).
    We must build the string with an accumulator loop.

    Rules:
    - Starts with '['
    - Numbers separated by ', ' except no comma+space after the last number
    - Ends with ']'
    - Works for empty list
    """
    if len(nums) == 0:
        return "[]"

    result = "["
    for i in range(len(nums)):
        # add current number
        result += str(nums[i])

        # for all except last, add ", "
        if i != len(nums) - 1:
            result += ", "
    result += "]"
    return result


def find_smallest_positive_multiple_of_three(nums):
    """
    find_smallest_positive_multiple_of_three(nums: list[int]) -> int or None

    Return the smallest integer in nums that:
    - is > 0
    - AND is a multiple of 3 (divisible evenly by 3)

    If there is no such number, return None.

    Pattern: optimization loop with conditional filter.
    We keep track of the "best so far" candidate.
    """
    candidate = None  # None means "we don't have a valid answer yet"

    for value in nums:
        # check "positive" and "multiple of 3"
        if value > 0 and (value % 3 == 0):
            if candidate is None or value < candidate:
                candidate = value

    return candidate


def sequential_search(target, nums):
    """
    sequential_search(target: int, nums: list[int]) -> bool

    Classic sequential search:
    - Look at each element in order.
    - If we see target, return True.
    - If we reach the end with no match, return False.

    This matches the pattern from class.
    """
    for x in nums:
        if x == target:
            return True
    return False


def binary_search(target, nums):
    """
    binary_search(target: int, nums: list[int]) -> bool

    Classic binary search on a SORTED list:
    - Keep low and high indexes.
    - Look at the middle.
    - Throw away half the search space each step.
    - Return True if found, False if we run out.

    Assumes nums is sorted in non-decreasing order.
    """
    low = 0
    high = len(nums) - 1

    while low <= high:
        mid = (low + high) // 2
        mid_val = nums[mid]

        if mid_val == target:
            return True
        elif mid_val < target:
            low = mid + 1
        else:
            high = mid - 1

    return False


def measure_search_times(list_size, strategy, shuffled, num_searches):
    """
    measure_search_times(list_size: int,
                         strategy: str ("sequential" or "binary"),
                         shuffled: bool,
                         num_searches: int)
        -> float (seconds, rounded to 6 decimals)

    What this does:
    1. Build a list [0, 1, 2, ..., list_size-1].
    2. If shuffled == True: random.shuffle(...) to scramble the list.
    3. Start timing.
       - If strategy == "binary" AND shuffled == True:
            sort the list ONCE using .sort(), but include that sorting time.
       - Then run 'num_searches' searches:
            * pick a random target from the list
            * call either sequential_search(...) or binary_search(...)
    4. Stop timing.
    5. Compute average time per single search:
            total_time / num_searches
       Return round(average_time, 6).

    Notes:
    - If list_size <= 0 or num_searches <= 0, return 0.0
    - binary_search requires the list to be sorted before searching
      (so we enforce that rule if shuffled is True).
    """
    if list_size <= 0 or num_searches <= 0:
        return 0.0

    nums = list(range(list_size))

    # Optionally shuffle the list *before* timing (spec says yes)
    if shuffled:
        random.shuffle(nums)

    # Start timer
    start_time = time.time()

    # If we are about to do binary search on a shuffled list, we must sort once
    # and include that cost in timing.
    if strategy == "binary" and shuffled:
        nums.sort()

    # Perform num_searches lookups, picking random targets from nums
    for _ in range(num_searches):
        # pick a random index in range [0, len(nums)-1]
        rand_index = random.randrange(0, len(nums))
        target = nums[rand_index]

        if strategy == "sequential":
            _ = sequential_search(target, nums)
        else:
            _ = binary_search(target, nums)

    total_elapsed = time.time() - start_time
    avg_time = total_elapsed / num_searches
    return round(avg_time, 6)


def main():
    # ---------------------------------------------------------
    # curve_scores tests
    # ---------------------------------------------------------
    print("=== curve_scores tests ===")

    scores1 = [45, 85, 90]
    expected1 = [55, 95, 100]  # max 90 -> shift +10
    actual1 = curve_scores(scores1)
    print("Input:", scores1)
    print("Expected:", expected1)
    print("Actual:  ", actual1)
    print()

    scores2 = [100, 90, 80]
    # max is 100 -> shift 0 -> same list
    expected2 = [100, 90, 80]
    actual2 = curve_scores(scores2)
    print("Input:", scores2)
    print("Expected:", expected2)
    print("Actual:  ", actual2)
    print()

    scores3 = []
    expected3 = []
    actual3 = curve_scores(scores3)
    print("Input:", scores3)
    print("Expected:", expected3)
    print("Actual:  ", actual3)
    print()

    # ---------------------------------------------------------
    # contains_duplicate tests
    # ---------------------------------------------------------
    print("=== contains_duplicate tests ===")

    words1 = ["the", "boy", "the"]
    expected_cd1 = True
    actual_cd1 = contains_duplicate(words1)
    print('Input:', words1)
    print("Expected:", expected_cd1)
    print("Actual:  ", actual_cd1)
    print()

    words2 = ["hi", "bye"]
    expected_cd2 = False
    actual_cd2 = contains_duplicate(words2)
    print('Input:', words2)
    print("Expected:", expected_cd2)
    print("Actual:  ", actual_cd2)
    print()

    words3 = []
    expected_cd3 = False
    actual_cd3 = contains_duplicate(words3)
    print('Input:', words3)
    print("Expected:", expected_cd3, "(empty list should be False)")
    print("Actual:  ", actual_cd3)
    print()

    words4 = ["a", "b", "c", "d", "e"]
    expected_cd4 = False
    actual_cd4 = contains_duplicate(words4)
    print('Input:', words4)
    print("Expected:", expected_cd4)
    print("Actual:  ", actual_cd4)
    print()

    # ---------------------------------------------------------
    # list_to_string tests
    # ---------------------------------------------------------
    print("=== list_to_string tests ===")

    lt1 = [1, 2, 3]
    expected_lt1 = "[1, 2, 3]"
    actual_lt1 = list_to_string(lt1)
    print("Input:", lt1)
    print("Expected:", expected_lt1)
    print("Actual:  ", actual_lt1)
    print()

    lt2 = []
    expected_lt2 = "[]"
    actual_lt2 = list_to_string(lt2)
    print("Input:", lt2)
    print("Expected:", expected_lt2)
    print("Actual:  ", actual_lt2)
    print()

    lt3 = [42]
    expected_lt3 = "[42]"
    actual_lt3 = list_to_string(lt3)
    print("Input:", lt3)
    print("Expected:", expected_lt3)
    print("Actual:  ", actual_lt3)
    print()

    # ---------------------------------------------------------
    # find_smallest_positive_multiple_of_three tests
    # ---------------------------------------------------------
    print("=== find_smallest_positive_multiple_of_three tests ===")

    f1 = [-3, 0, 2, 3, 1, 6]
    expected_f1 = 3  # 3 and 6 are >0 and mult of 3, smallest is 3
    actual_f1 = find_smallest_positive_multiple_of_three(f1)
    print("Input:", f1)
    print("Expected:", expected_f1)
    print("Actual:  ", actual_f1)
    print()

    f2 = [9, 12, 3, 30]
    expected_f2 = 3  # smallest positive multiple of 3 is 3
    actual_f2 = find_smallest_positive_multiple_of_three(f2)
    print("Input:", f2)
    print("Expected:", expected_f2)
    print("Actual:  ", actual_f2)
    print()

    f3 = [1, 2, 4, 5, 7]
    expected_f3 = None  # none of these are multiples of 3
    actual_f3 = find_smallest_positive_multiple_of_three(f3)
    print("Input:", f3)
    print("Expected:", expected_f3)
    print("Actual:  ", actual_f3)
    print()

    f4 = [-9, -6, -3, 0]
    expected_f4 = None  # there are multiples of 3 but none > 0
    actual_f4 = find_smallest_positive_multiple_of_three(f4)
    print("Input:", f4)
    print("Expected:", expected_f4)
    print("Actual:  ", actual_f4)
    print()

    # ---------------------------------------------------------
    # sequential_search and binary_search tests
    # ---------------------------------------------------------
    print("=== sequential_search / binary_search tests ===")

    nums_search = [2, 5, 10, 20]

    # sequential_search tests
    expected_seq1 = True
    actual_seq1 = sequential_search(10, nums_search)
    print("sequential_search(10, [2,5,10,20])")
    print("Expected:", expected_seq1)
    print("Actual:  ", actual_seq1)
    print()

    expected_seq2 = False
    actual_seq2 = sequential_search(99, nums_search)
    print("sequential_search(99, [2,5,10,20])")
    print("Expected:", expected_seq2)
    print("Actual:  ", actual_seq2)
    print()

    # binary_search tests (list must be sorted; nums_search is sorted)
    expected_bin1 = True
    actual_bin1 = binary_search(10, nums_search)
    print("binary_search(10, [2,5,10,20])")
    print("Expected:", expected_bin1)
    print("Actual:  ", actual_bin1)
    print()

    expected_bin2 = False
    actual_bin2 = binary_search(99, nums_search)
    print("binary_search(99, [2,5,10,20])")
    print("Expected:", expected_bin2)
    print("Actual:  ", actual_bin2)
    print()

    # Another binary test with longer list
    nums_search2 = [1, 4, 7, 9, 12, 15, 30, 31]
    expected_bin3 = True
    actual_bin3 = binary_search(1, nums_search2)
    print("binary_search(1, [1,4,7,9,12,15,30,31])")
    print("Expected:", expected_bin3)
    print("Actual:  ", actual_bin3)
    print()

    expected_bin4 = False
    actual_bin4 = binary_search(8, nums_search2)
    print("binary_search(8, [1,4,7,9,12,15,30,31])")
    print("Expected:", expected_bin4)
    print("Actual:  ", actual_bin4)
    print()

    # ---------------------------------------------------------
    # measure_search_times informal timing demo
    # (We can't "expect" an exact number, so just show usage.)
    # ---------------------------------------------------------
    print("=== measure_search_times demo (timing will vary) ===")
    avg_seq_sorted = measure_search_times(
        list_size=2000,
        strategy="sequential",
        shuffled=False,
        num_searches=200
    )
    print("Avg time per search (sequential, sorted list):", avg_seq_sorted)

    avg_bin_sorted = measure_search_times(
        list_size=2000,
        strategy="binary",
        shuffled=False,
        num_searches=200
    )
    print("Avg time per search (binary, already sorted list):", avg_bin_sorted)

    avg_seq_shuffled = measure_search_times(
        list_size=2000,
        strategy="sequential",
        shuffled=True,
        num_searches=200
    )
    print("Avg time per search (sequential, shuffled list):", avg_seq_shuffled)

    avg_bin_shuffled = measure_search_times(
        list_size=2000,
        strategy="binary",
        shuffled=True,
        num_searches=200
    )
    print("Avg time per search (binary, shuffled list first then sort once):", avg_bin_shuffled)


if __name__ == "__main__":
    main()
