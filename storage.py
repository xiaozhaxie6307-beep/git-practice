import json
from pathlib import Path
from uuid import uuid4


DATA_FILE = Path(__file__).with_name("records.json")


def save_records(records, path=DATA_FILE):
    """先写临时文件，写完再替换正式文件。"""
    temp_path = path.with_suffix(".json.tmp")
    try:
        with temp_path.open("w", encoding="utf-8") as file:
            json.dump(records, file, ensure_ascii=False, indent=2)
        temp_path.replace(path)
    finally:
        temp_path.unlink(missing_ok=True)


def validate_record(record, number):
    """检查从文件中读到的主题与分钟数。"""
    if not isinstance(record, dict):
        raise ValueError(f"第 {number} 条记录必须是字典。")

    topic = record.get("topic")
    if not isinstance(topic, str) or not topic.strip():
        raise ValueError(f"第 {number} 条记录的主题无效。")

    minutes = record.get("minutes")
    if type(minutes) is not int or minutes <= 0:
        raise ValueError(f"第 {number} 条记录的分钟数无效。")


def new_record_id(used_ids):
    """生成一个当前列表中未使用的 ID。"""
    record_id = uuid4().hex
    while record_id in used_ids:
        record_id = uuid4().hex
    return record_id


def load_records(path=DATA_FILE):
    """首次启动返回空列表，格式错误由入口统一提示。"""
    try:
        with path.open("r", encoding="utf-8") as file:
            records = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise ValueError(
            f"{path.name} 的 JSON 无效（第 {error.lineno} 行，第 {error.colno} 列）。"
        ) from error
    except UnicodeDecodeError as error:
        raise ValueError(f"{path.name} 需要使用 UTF-8 编码。") from error

    if not isinstance(records, list):
        raise ValueError(f"{path.name} 最外层必须是列表。")
    used_ids = set()
    for number, record in enumerate(records, start=1):
        validate_record(record, number)
        if "id" in record:
            record_id = record["id"]
            if not isinstance(record_id, str) or not record_id.strip():
                raise ValueError(f"第 {number} 条记录的 ID 无效。")
            if record_id in used_ids:
                raise ValueError(f"第 {number} 条记录的 ID 重复。")
            used_ids.add(record_id)

    # 全部检查成功后，才补齐旧记录的字段。
    changed = False
    for record in records:
        if "id" not in record:
            record_id = new_record_id(used_ids)
            record["id"] = record_id
            used_ids.add(record_id)
            changed = True

    if changed:
        save_records(records, path)
    return records