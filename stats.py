def total_minutes(records):
    """返回记录列表的总分钟数。"""
    total = 0
    for record in records:
        total += record["minutes"]
    return total


def minutes_by_topic(records, topic):
    """只累加主题匹配的记录。"""
    total = 0
    for record in records:
        if record["topic"] == topic:
            total += record["minutes"]
    return total