def validate_items(items, tolerance=0.01):
    inconsistencies = []
    for idx, item in enumerate(items):
        if all(k in item for k in ["quantity", "unit_price", "total_price"]):
            expected = round(item["quantity"] * item["unit_price"], 2)
            actual = round(item["total_price"], 2)
            if abs(expected - actual) > tolerance:
                inconsistencies.append({
                    "index": idx,
                    "expected_total": expected,
                    "actual_total": actual,
                    "item": item
                })

    return inconsistencies