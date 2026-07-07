def calculate_fraud_cost(y_true, y_pred, amounts, review_cost=10):
    """
    Calculates total financial cost of a fraud detection model's predictions.

    False Negative (missed fraud): cost = actual transaction amount, the real loss.
    False Positive (false alarm): cost = fixed review cost, the operational cost of investigating a flagged transaction.
    True Positive (caught fraud): cost = review cost only, since the loss was avoided.
    True Negative: no cost.

    Parameters:
    y_true: actual labels (0 = genuine, 1 = fraud)
    y_pred: predicted labels (0 = genuine, 1 = fraud)
    amounts: transaction amounts, same order as y_true/y_pred
    review_cost: fixed cost of manually reviewing a flagged transaction

    Returns:
    dict with total cost and cost breakdown by category
    """
    total_cost = 0
    false_negative_cost = 0
    false_positive_cost = 0
    true_positive_cost = 0

    for actual, predicted, amount in zip(y_true, y_pred, amounts):
        if actual == 1 and predicted == 0:
            false_negative_cost += amount
        elif actual == 0 and predicted == 1:
            false_positive_cost += review_cost
        elif actual == 1 and predicted == 1:
            true_positive_cost += review_cost

    total_cost = false_negative_cost + false_positive_cost + true_positive_cost

    return {
        "total_cost": total_cost,
        "false_negative_cost": false_negative_cost,
        "false_positive_cost": false_positive_cost,
        "true_positive_cost": true_positive_cost
    }