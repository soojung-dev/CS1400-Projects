# A10.py
# Assignment 10: Recursion Practice
# Written by Soojung Kim, Junghee Kim


# ======================================================================================
# Recursive Functions
# ======================================================================================


def compute_power(base_num, power_num):
    """
    Compute the value of base_num raised to the power of power_num recursively.

    :param base_num: The base number (positive integer).
    :param power_num: The exponent (positive integer).
    :return: Result of base_num ** power_num.
    """
    if power_num == 0:  # base case
        return 1
    return base_num * compute_power(base_num, power_num - 1)  # recursive case



def total_bunny_ears(bunnies):
    """
    Compute the total number of ears for a given number of bunnies (2 ears each).

    :param bunnies: Number of bunnies.
    :return: Total number of bunny ears.
    """
    if bunnies == 0:  # base case
        return 0
    return 2 + total_bunny_ears(bunnies - 1)  # recursive case



def number_of_blocks(rows_of_triangle):
    """
    Compute the total number of blocks in a triangle with a given number of rows.

    :param rows_of_triangle: Number of rows in the triangle.
    :return: Total number of blocks.
    """
    if rows_of_triangle == 0:  # base case
        return 0
    return rows_of_triangle + number_of_blocks(rows_of_triangle - 1)  # recursive case



def sum_digits(num):
    """
    Compute the sum of all digits in a non-negative integer.

    :param num: Non-negative integer.
    :return: Sum of all digits.
    """
    if num == 0:  # base case
        return 0
    return num % 10 + sum_digits(num // 10)  # recursive case



def count_7(num):
    """
    Count the total number of times the digit 7 appears in a non-negative integer.

    :param num: Non-negative integer.
    :return: Number of times 7 appears.
    """
    if num == 0:  # base case
        return 0
    return int(num % 10 == 7) + count_7(num // 10)  # recursive case



def change_x_to_y(word):
    """
    Change all occurrences of the lowercase letter 'x' to 'y' in a string.

    :param word: A lowercase string.
    :return: New string with 'x' replaced by 'y'.
    """
    if word == "":  # base case
        return ""

    # recursive case
    if word[0] == 'x':
        return 'y' + change_x_to_y(word[1:])
    else:
        return word[0] + change_x_to_y(word[1:])



def change_hi_to_bye(sent):
    """
    Replace all occurrences of 'hi' with 'bye' in a string.

    :param sent: A lowercase string.
    :return: New string with 'hi' replaced by 'bye'.
    """
    if sent == "":  # base case
        return ""

    # recursive case
    if sent[0:2] == "hi":
        return "bye" + change_hi_to_bye(sent[2:])

    else:
        return sent[0] + change_hi_to_bye(sent[1:])



def add_stars(word):
    """
    Add '*' between all adjacent characters in a string.

    :param word: A lowercase string.
    :return: New string with '*' between each character.
    """
    if len(word) <= 1:  # base case
        return word
    return(word[0] + "*" + add_stars(word[1:]))  # recursive case



def pair_stars(word):
    """
    Add '*' between adjacent identical characters in a string.

    :param word: A lowercase string.
    :return: New string with '*' between repeating characters.
    """
    if len(word) <= 1:  # base case
        return word
    return (word[0] + '*' + pair_stars(word[1:]) if word[0] == word[1] else (word[0] + pair_stars(word[1:])))  # recursive case



def contains_7(nums):
    """
    Determine whether a list of integers contains the integer 7.

    :param nums: List of integers.
    :return: True if list contains 7, False otherwise.
    """
    if len(nums) == 0:  # base case
        return False
    return (True) if nums[0] == 7 else contains_7(nums[1:])  # recursive case



def count_occurrences(lst, target):
    """
    Count the number of times a target value appears in a list.

    :param lst: List of elements.
    :param target: The value to count.
    :return: Number of times target appears.
    """
    if len(lst) == 0:  # base case
        return 0
    return int(lst[0] == target) + count_occurrences(lst[1:], target)  # recursive case





# ======================================================================================
# Testing the functions with Expected values
# ======================================================================================


def main():
    # New examples for testing with Expected values
    print("compute_power(2, 5) =", compute_power(2, 5), ", Expected: 32")
    print("total_bunny_ears(6) =", total_bunny_ears(6), ", Expected: 12")
    print("number_of_blocks(5) =", number_of_blocks(5), ", Expected: 15")
    print("sum_digits(4567) =", sum_digits(4567), ", Expected: 22")
    print("count_7(77077) =", count_7(77077), ", Expected: 4")
    print("change_x_to_y('xenon') =", change_x_to_y("xenon"), ", Expected: 'yenon'")
    print("change_hi_to_bye('hiking hi') =", change_hi_to_bye("hiking hi"), ", Expected: 'byeking bye'")
    print("add_stars('python') =", add_stars("python"), ", Expected: 'p*y*t*h*o*n'")
    print("pair_stars('bookkeeper') =", pair_stars("bookkeeper"), ", Expected: 'book*keep*er'")
    print("contains_7([4, 1, 7, 9]) =", contains_7([4, 1, 7, 9]), ", Expected: True")
    print("count_occurrences([3,5,3,3,2], 3) =", count_occurrences([3, 5, 3, 3, 2], 3), ", Expected: 3")


if __name__ == "__main__":
    main()