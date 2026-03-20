# CS 1400
# Assignment 6: Sound Effects
# Written by Soojung Kim, Junghee Kim
#
# This file defines helper functions that operate on lists of integer samples
# to create simple audio effects. Each function returns a NEW list and does not
# mutate the input list. A small test suite is provided in main().
#
# NOTE: Implementations use only loops/conditionals and built-in types
# (no list comprehensions, no slicing tricks).

import random


def make_reversed_samples(samples):
    """Return a NEW list containing the elements of samples in reverse order."""
    new_list = []
    i = len(samples) - 1
    while i >= 0:
        new_list.append(samples[i])
        i -= 1
    return new_list


def make_louder_samples(samples, scale):
    """Return a NEW list where each element is multiplied by the integer scale."""
    new_list = []
    i = 0
    while i < len(samples):
        new_list.append(samples[i] * scale)
        i += 1
    return new_list


def make_clipped_samples(samples, clip_level):
    """Return a NEW list where each value is limited to [-clip_level, clip_level]."""
    new_list = []
    i = 0
    while i < len(samples):
        val = samples[i]
        if val > clip_level:
            new_list.append(clip_level)
        elif val < -clip_level:
            new_list.append(-clip_level)
        else:
            new_list.append(val)
        i += 1
    return new_list


def make_noisy_samples(samples, noise_level):
    """Return a NEW list where random integer noise in [-noise_level, noise_level]
    is added to each element."""
    noisy_list = []
    i = 0
    while i < len(samples):
        noise = random.randint(-noise_level, noise_level)
        noisy_list.append(samples[i] + noise)
        i += 1
    return noisy_list


def make_smoothed_samples(samples):
    """Return a NEW list where each value is the integer average of its neighbors.
       First = avg of first two, Last = avg of last two, Middle = avg of three."""
    n = len(samples)
    new_list = []

    if n == 0:
        return []
    if n == 1:
        # Degenerate case: just return a copy
        return [samples[0]]
    if n == 2:
        # Average of each adjacent pair is the same for both ends
        avg = int((samples[0] + samples[1]) / 2)
        return [avg, avg]

    # First: avg of first two
    first_avg = int((samples[0] + samples[1]) / 2)
    new_list.append(first_avg)

    # Middle
    i = 1
    while i < n - 1:
        avg = int((samples[i - 1] + samples[i] + samples[i + 1]) / 3)
        new_list.append(avg)
        i += 1

    # Last
    last_avg = int((samples[n - 2] + samples[n - 1]) / 2)
    new_list.append(last_avg)

    return new_list


def make_echo_samples(samples, offset, weight):
    """Return a NEW list with an echo effect applied."""
    new_list = []
    n = len(samples)

    # 1) Original section
    i = 0
    while i < offset and i < n:
        new_list.append(samples[i])
        i += 1

    # 2) Echoed section
    i = offset
    while i < n:
        new_val = int(samples[i] + samples[i - offset] * weight)
        new_list.append(new_val)
        i += 1

    # 3) Tail section
    i = n - offset
    while i < n:
        tail_val = int(weight * samples[i])
        new_list.append(tail_val)
        i += 1

    return new_list


def main():
    print("=== Testing make_reversed_samples ===")
    data = [1, 2, 3, 4]
    print("Input:", data)
    print("Expected:", [4, 3, 2, 1])
    print("Actual:", make_reversed_samples(data))

    print("\n=== Testing make_louder_samples ===")
    data = [10, -5, 0]
    print("Input:", data)
    print("Expected:", [30, -15, 0])
    print("Actual:", make_louder_samples(data, 3))

    print("\n=== Testing make_clipped_samples ===")
    data = [-5, -1, 2, 5, 10]
    print("Input:", data)
    print("Expected:", [-4, -1, 2, 4, 4])
    print("Actual:", make_clipped_samples(data, 4))

    print("\n=== Testing make_noisy_samples ===")
    random.seed(42)
    data = [10, 20, 30]
    print("Input:", data)
    print("Result:", make_noisy_samples(data, 2))

    print("\n=== Testing make_smoothed_samples ===")
    data = [0, 100, 500, -100]
    print("Input:", data)
    print("Expected:", [50, 200, 166, 200])
    print("Actual:", make_smoothed_samples(data))

    print("\n=== Testing make_echo_samples ===")
    data = [10, 20, 30, 40]
    print("Input:", data)
    print("Expected (offset=1, weight=0.5):", [10, 25, 40, 55, 20])
    print("Actual:", make_echo_samples(data, 1, 0.5))
    print("Expected (offset=2, weight=0.5):", [10, 20, 35, 50, 15, 20])
    print("Actual:", make_echo_samples(data, 2, 0.5))


if __name__ == "__main__":
    main()