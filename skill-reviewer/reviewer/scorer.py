def calculate_score(validation_issues, ai_review):
    score = 100

    #
    # STATIC PENALTIES (authoritative)
    #

    issue_penalty = len(validation_issues) * 20
    score -= issue_penalty

    #
    # AI REVIEW (influence)
    #

    clarity = ai_review.get("clarity", 5)
    completeness = ai_review.get("completeness", 5)
    maintainability = ai_review.get("maintainability", 5)
    ambiguity = ai_review.get("ambiguity", 5)

    # Weighted average. Clarity and completeness are more important.
    ai_average = (
        (clarity * 1.2) +
        (completeness * 1.2) +
        maintainability
    ) / 3.4

    #
    # AI adjustment
    #
    if ai_average >= 8:
        score += 10
    elif ai_average >= 6:
        score += 5
    elif ai_average <= 4:
        score -= 10
    elif ai_average <= 2:
        score -= 20


    #
    # Ambiguity penalty
    #
    if ambiguity >= 8:
        score -= 20
    elif ambiguity >= 6:
        score -= 10

    return max(0, min(100, round(score)))
