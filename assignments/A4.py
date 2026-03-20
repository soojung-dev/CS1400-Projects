# A4.py
# Assignment completed by: Junghee Kim & Soojung Kim
# This file implements several functions and tests them from main().

# ------------------------------------------------------------
# 1) choose_larger
# Return the larger of two numeric parameters (if equal, return either).
def choose_larger(num1, num2):
    if num1 >= num2:
        return num1
    else:
        return num2


# ------------------------------------------------------------
# 2) triangle_type
# Classify triangle by side lengths: "Equilateral", "Isosceles", "Scalene".
def triangle_type(side1, side2, side3):
    if side1 == side2 and side2 == side3:
        return "Equilateral"
    elif side1 == side2 or side2 == side3 or side1 == side3:
        return "Isosceles"
    else:
        return "Scalene"


# ------------------------------------------------------------
# 3) add_a_or_an_to_word
# Given a lowercase word, prefix "an " if it starts with a vowel (a e i o u), else "a ".
def add_a_or_an_to_word(word):
    first = word[0]
    if first == 'a' or first == 'e' or first == 'i' or first == 'o' or first == 'u':
        return "an " + word
    else:
        return "a " + word


# ------------------------------------------------------------
# 4) add_a_or_an_or_any_to_word
# Like above, but if the last letter is 's', use "any ".
def add_a_or_an_or_any_to_word(word):
    if word[-1] == 's':
        return "any " + word
    # otherwise same rule as add_a_or_an_to_word
    else:
        return add_a_or_an_to_word(word)


# ------------------------------------------------------------
# 5) replace_in_list
# Return a new list where every element equal to old_value is replaced with new_value.
# Must use an index-based loop (no list comprehension, no enumerate).
def replace_in_list(lst, old_value, new_value):
    result = list(lst)  # copy so we don't mutate caller's list
    for i in range(len(result)):
        if result[i] == old_value:
            result[i] = new_value
    return result


# ------------------------------------------------------------
# 6) replace_word_with_synonym
# Given one lowercase word, return its synonym if known, else the original word.
# (Use if/elif chains only; do not use sets/dicts not discussed yet.)
def replace_word_with_synonym(word):
    if word == "big":
        return "vast"
    elif word == "important":
        return "noteworthy"
    elif word == "quiet":
        return "tranquil"
    elif word == "nice":
        return "pleasant"
    elif word == "quick" or word == "fast":
        return "prompt"
    elif word == "funny":
        return "humorous"
    elif word == "kind":
        return "benevolent"
    elif word == "fun":
        return "exhilarating"
    elif word == "brave":
        return "courageous"
    elif word == "exciting":
        return "thrilling"
    else:
        return word


# ------------------------------------------------------------
# 7) thesaurus
# Given a lowercase sentence without punctuation, replace each word with its synonym (if known)
# using split -> per-word replacement with replace_word_with_synonym -> join.
def thesaurus(sentence):
    words = sentence.split()
    for i in range(len(words)):
        words[i] = replace_word_with_synonym(words[i])
    return " ".join(words)


# ------------------------------------------------------------
# main: print clear tests for each function (what/args/expected/actual).
def main():
    print("=== Testing choose_larger ===")
    a, b = 10, 20
    expected = 20
    actual = choose_larger(a, b)
    print(f"Args: {a}, {b} | Expected: {expected} | Actual: {actual}")
    a, b = -5, -5
    expected = -5
    actual = choose_larger(a, b)
    print(f"Args: {a}, {b} | Expected: {expected} | Actual: {actual}")
    a, b = 7.2, 3.9
    expected = 7.2
    actual = choose_larger(a, b)
    print(f"Args: {a}, {b} | Expected: {expected} | Actual: {actual}")

    print("\n=== Testing triangle_type ===")
    sides = (5, 5, 5)
    expected = "Equilateral"
    actual = triangle_type(*sides)
    print(f"Args: {sides} | Expected: {expected} | Actual: {actual}")
    sides = (5, 3, 5)
    expected = "Isosceles"
    actual = triangle_type(*sides)
    print(f"Args: {sides} | Expected: {expected} | Actual: {actual}")
    sides = (2, 3, 4)
    expected = "Scalene"
    actual = triangle_type(*sides)
    print(f"Args: {sides} | Expected: {expected} | Actual: {actual}")

    print("\n=== Testing add_a_or_an_to_word ===")
    word = "ant"
    expected = "an ant"
    actual = add_a_or_an_to_word(word)
    print(f"Arg: {word} | Expected: {expected} | Actual: {actual}")
    word = "dog"
    expected = "a dog"
    actual = add_a_or_an_to_word(word)
    print(f"Arg: {word} | Expected: {expected} | Actual: {actual}")
    word = "umbrella"
    expected = "an umbrella"
    actual = add_a_or_an_to_word(word)
    print(f"Arg: {word} | Expected: {expected} | Actual: {actual}")

    print("\n=== Testing add_a_or_an_or_any_to_word ===")
    word = "cats"
    expected = "any cats"
    actual = add_a_or_an_or_any_to_word(word)
    print(f"Arg: {word} | Expected: {expected} | Actual: {actual}")
    word = "apple"
    expected = "an apple"
    actual = add_a_or_an_or_any_to_word(word)
    print(f"Arg: {word} | Expected: {expected} | Actual: {actual}")
    word = "banana"
    expected = "a banana"
    actual = add_a_or_an_or_any_to_word(word)
    print(f"Arg: {word} | Expected: {expected} | Actual: {actual}")

    print("\n=== Testing replace_in_list ===")
    src = [0, 1, "hi", 4.7, 1, 1]
    expected = [0, "bye", "hi", 4.7, "bye", "bye"]
    actual = replace_in_list(src, 1, "bye")
    print(f"Args: {src}, old=1, new='bye' | Expected: {expected} | Actual: {actual}")
    src = ["a", "b", "a", "c"]
    expected = ["x", "b", "x", "c"]
    actual = replace_in_list(src, "a", "x")
    print(f"Args: {src}, old='a', new='x' | Expected: {expected} | Actual: {actual}")

    print("\n=== Testing replace_word_with_synonym ===")
    word = "fun"
    expected = "exhilarating"
    actual = replace_word_with_synonym(word)
    print(f"Arg: {word} | Expected: {expected} | Actual: {actual}")
    word = "fast"
    expected = "prompt"
    actual = replace_word_with_synonym(word)
    print(f"Arg: {word} | Expected: {expected} | Actual: {actual}")
    word = "unknownword"
    expected = "unknownword"
    actual = replace_word_with_synonym(word)
    print(f"Arg: {word} | Expected: {expected} | Actual: {actual}")

    print("\n=== Testing thesaurus ===")
    sentence = "this is a big important function"
    expected = "this is a vast noteworthy function"
    actual = thesaurus(sentence)
    print(f"Arg: '{sentence}' | Expected: '{expected}' | Actual: '{actual}'")
    sentence = "you are funny and kind"
    expected = "you are humorous and benevolent"
    actual = thesaurus(sentence)
    print(f"Arg: '{sentence}' | Expected: '{expected}' | Actual: '{actual}'")
    sentence = "how exciting"
    expected = "how thrilling"
    actual = thesaurus(sentence)
    print(f"Arg: '{sentence}' | Expected: '{expected}' | Actual: '{actual}'")

    print("\n=== Extra edge tests ===")
    print("Arg: as | Expected: any as | Actual:", add_a_or_an_or_any_to_word("as"))
    print("Arg: 'quick and fast fun' | Expected: 'prompt and prompt exhilarating' | Actual:",
      thesaurus("quick and fast fun"))



if __name__ == "__main__":
    main()