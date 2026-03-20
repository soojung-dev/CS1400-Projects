# CS 1400 — Assignment 8: RateMyProfessors Data Analysis
# Authors: Junghee Kim (u1558274), Soojung Kim
#
# IMPORTANT:
# - Implementations follow the assignment spec exactly (function names/params unchanged).
# - Do NOT modify rmpvisualization.py. It will import these functions.
# - Test with small-data.txt first. Then (temporarily) switch to full-data.txt,
#   write your 1–2 sentence interpretation in the comment below, and switch back.

from typing import List, Dict


def get_lines_from_file(filename: str) -> List[str]:
    """
    Open the given file and return a list of its data lines (skip the header row).

    Parameters
    ----------
    filename : str
        Path to a CSV-like text file whose first line is a header.

    Returns
    -------
    List[str]
        All lines EXCEPT the first header line, in original order.
        Each element includes the trailing newline if present in the file.
    """
    with open(filename, "r", encoding="utf-8") as f:
        lines = f.readlines()
    # Skip header row
    return lines[1:]


def get_reviews_for_gender(lines: List[str], target_gender: str) -> List[List[str]]:
    """
    Filter the raw data lines by gender and return structured rows of [rating, gender, comment].

    Parameters
    ----------
    lines : List[str]
        Raw data lines (excluding header), each like "4.5,W,nice smile but nice".
    target_gender : str
        'M' for Man or 'W' for Woman.

    Returns
    -------
    List[List[str]]
        Rows formatted as [rating_str, gender_str, comment_str] ONLY for target_gender.
    """
    results: List[List[str]] = []
    for line in lines:
        clean = line.strip()
        if not clean:
            continue
        # Split into exactly 3 parts: rating, gender, comment (comment may contain commas in other datasets;
        # here it's cleaned, but split(',', 2) is safer and matches the spec).
        parts = clean.split(",", 2)
        if len(parts) != 3:
            continue
        rating_str, gender_str, comment_str = parts[0].strip(), parts[1].strip(), parts[2].strip()
        if gender_str == target_gender:
            results.append([rating_str, gender_str, comment_str])
    return results


def categorize_reviews(score) -> int:
    """
    Map a numeric review score to a category bucket.

    Buckets:
      - 0: low   (< 2.5)
      - 1: medium( 2.5–3.5 inclusive )
      - 2: high  (> 3.5)

    Parameters
    ----------
    score : Any
        int/float/str accepted. String numbers like '3.0' are valid.

    Returns
    -------
    int
        0, 1, or 2 according to the spec.
        If parsing fails, treat as medium (conservative default).
    """
    try:
        value = float(score)
    except (TypeError, ValueError):
        value = 3.0  # fall back to medium
    if value < 2.5:
        return 0
    elif value <= 3.5:
        return 1
    else:
        return 2


def calculate_rating_stats(reviews: List[List[str]], target_rating_category: int) -> int:
    """
    Calculate the percentage of reviews that fall into the target rating category.

    Calculation:
        percent = round( (count_in_category / total_reviews) * 100 )

    Parameters
    ----------
    reviews : List[List[str]]
        Each inner list is [rating_str, gender, comment].
    target_rating_category : int
        0 (low), 1 (medium), or 2 (high).

    Returns
    -------
    int
        Rounded integer percent. Returns 0 if reviews is empty.
    """
    if not reviews:
        return 0
    total = len(reviews)
    count_in_bucket = 0
    for rating_str, _gender, _comment in reviews:
        if categorize_reviews(rating_str) == target_rating_category:
            count_in_bucket += 1
    pct = (count_in_bucket / total) * 100.0
    return int(round(pct))


def add_data_for_word(word_data: Dict[str, List[int]], word: str, score) -> None:
    """
    Add or update a word entry in the dictionary based on the review score.

    word_data maps:
        word (str) -> [low_count, medium_count, high_count]

    Parameters
    ----------
    word_data : Dict[str, List[int]]
        Mutable dictionary to update.
    word : str
        Token from the comment text (already lowercase/cleaned by dataset).
    score : Any
        Numeric score (str/float/int). Will be categorized via categorize_reviews.

    Returns
    -------
    None
        Mutates word_data in place.
    """
    idx = categorize_reviews(score)
    if word not in word_data:
        word_data[word] = [0, 0, 0]
    word_data[word][idx] += 1


def format_to_dict(review_data: List[List[str]]) -> Dict[str, List[int]]:
    """
    Build a dictionary of word frequencies categorized by review rating.

    Parameters
    ----------
    review_data : List[List[str]]
        Rows formatted as [rating_str, gender_str, comment_str] for ONE gender.

    Returns
    -------
    Dict[str, List[int]]
        word -> [low_count, medium_count, high_count]
    """
    word_data: Dict[str, List[int]] = {}
    for rating_str, _gender, comment in review_data:
        # comment is cleaned: lowercase, no punctuation; tokens are space-separated.
        for token in comment.split():
            if token:  # guard against empty tokens (defensive)
                add_data_for_word(word_data, token, rating_str)
    return word_data


def search_words(word_dict: Dict[str, List[int]], target_string: str) -> List[str]:
    """
    Return all words in the dictionary that contain the target substring (case-insensitive).

    Parameters
    ----------
    word_dict : Dict[str, List[int]]
        Dictionary produced by format_to_dict.
    target_string : str
        Substring to match anywhere in the word.

    Returns
    -------
    List[str]
        All matching words. Sorted alphabetically for usability.
    """
    target = (target_string or "").lower()
    matches: List[str] = []
    if not target:
        return matches
    for word in word_dict.keys():
        if target in word.lower():
            matches.append(word)
    return sorted(matches)


def _demo_small_dataset() -> None:
    """
    Simple console demo using small-data.txt (optional helper for manual checks).
    """
    import os
    fname = "small-data.txt"
    if not os.path.exists(fname):
        print("[demo] small-data.txt not found.")
        return

    print("[demo] Loading lines from small-data.txt...")
    lines = get_lines_from_file(fname)
    men = get_reviews_for_gender(lines, "M")
    women = get_reviews_for_gender(lines, "W")

    for label, reviews in [("M", men), ("W", women)]:
        low = calculate_rating_stats(reviews, 0)
        med = calculate_rating_stats(reviews, 1)
        high = calculate_rating_stats(reviews, 2)
        print(f"{label}: low={low}%, med={med}%, high={high}%")

    wdict = format_to_dict(women)
    mdict = format_to_dict(men)
    print("[demo] women dict:", wdict)
    print("[demo] men dict  :", mdict)
    print('[demo] search "ni" in women:', search_words(wdict, "ni"))
    print('[demo] search "bor" in men  :', search_words(mdict, "bor"))


def main() -> None:
    # ======================= ANALYSIS COMMENT =======================
    # After running ONCE with data_file="full-data.txt", record your 1–2 line
    # interpretation here (then switch back to small-data.txt for testing):
    #
    # Example format to replace:
    # For the full dataset (2001–2018), high reviews were XX% for women vs. YY% for men,
    # while low reviews were AA% for women vs. BB% for men.
    # This suggests (your brief interpretation here).
    # ================================================================

    data_file = "small-data.txt"
    # To test full dataset temporarily:
    # data_file = "full-data.txt"

    try:
        lines = get_lines_from_file(data_file)
    except FileNotFoundError:
        print(f"[error] Could not find {data_file}.")
        return

    men_reviews = get_reviews_for_gender(lines, "M")
    women_reviews = get_reviews_for_gender(lines, "W")
    print(f"Total men reviews: {len(men_reviews)} | Total women reviews: {len(women_reviews)}")

    for label, reviews in [("Men", men_reviews), ("Women", women_reviews)]:
        low = calculate_rating_stats(reviews, 0)
        med = calculate_rating_stats(reviews, 1)
        high = calculate_rating_stats(reviews, 2)
        print(f"{label} — Low: {low}% | Medium: {med}% | High: {high}%")

    # Build dictionaries for visualization module
    men_dict = format_to_dict(men_reviews)
    women_dict = format_to_dict(women_reviews)

    # Lightweight interactive search for manual checks (optional).
    import sys
    is_tty = hasattr(sys.stdin, "isatty") and sys.stdin.isatty()

    if is_tty:
        while True:
            try:
                q = input('\n[search] Enter a substring to search (or Enter to quit): ').strip()
            except EOFError:
                break
            if not q:
                break
            print("Women matches:", search_words(women_dict, q))
            print("Men matches  :", search_words(men_dict, q))

            word = input("[plot] Enter EXACT word to view raw counts (or Enter to skip): ").strip().lower()
            if not word:
                continue
            w_counts = women_dict.get(word)
            m_counts = men_dict.get(word)
            print(f"Raw counts for '{word}'  (W: [low, med, high]) -> {w_counts}")
            print(f"Raw counts for '{word}'  (M: [low, med, high]) -> {m_counts}")


if __name__ == "__main__":
    main()
