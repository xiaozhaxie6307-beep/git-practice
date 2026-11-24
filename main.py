from stats import minutes_by_topic, total_minutes
from storage import load_records, new_record_id, save_records


def parse_topic(text):
    topic = text.strip()
    if not topic:
        raise ValueError("主题不能为空。")
    return topic


def parse_minutes(text):
    try:
        minutes = int(text)
    except ValueError:
        raise ValueError("分钟数必须是正整数。") from None
    if minutes <= 0:
        raise ValueError("分钟数必须大于 0。")
    return minutes


def read_new_record():
    topic = parse_topic(input("主题："))
    minutes = parse_minutes(input("分钟数："))
    record = {"topic": topic, "minutes": minutes}
    return record


def show_records(records):
    if not records:
        print("没有匹配的记录。")
        return

    for record in records:
        print(f"ID {record['id']} · {record['topic']}：{record['minutes']} 分钟")


def delete_by_id(records, record_id):
    """找到完整 ID 时删除一条记录，并报告是否找到。"""
    for index, record in enumerate(records):
        if record["id"] == record_id:
            records.pop(index)
            return True
    return False


def show_menu():
    print("\n1. 添加记录")
    print("2. 查看记录")
    print("3. 统计全部")
    print("4. 按主题统计")
    print("5. 按 ID 删除")
    print("0. 退出")


def main():
    records = load_records()
    while True:
        show_menu()
        choice = input("请选择：").strip()

        try:
            if choice == "0":
                print("已退出。")
                break
            elif choice == "1":
                record = read_new_record()
                used_ids = set()
                for saved_record in records:
                    used_ids.add(saved_record["id"])
                record["id"] = new_record_id(used_ids)
                records.append(record)
                save_records(records)
                print(f"添加成功，记录 ID：{record['id']}。")
            elif choice == "2":
                show_records(records)
            elif choice == "3":
                print(f"全部学习时长：{total_minutes(records)} 分钟")
            elif choice == "4":
                topic = parse_topic(input("要统计的主题："))
                print(f"{topic}：{minutes_by_topic(records, topic)} 分钟")
            elif choice == "5":
                record_id = input("要删除的完整 ID：").strip()
                if delete_by_id(records, record_id):
                    save_records(records)
                    print("已删除。")
                else:
                    print("未找到该 ID。")
            else:
                print("无效选项，请重新选择。")
        except ValueError as error:
            print(f"输入无效：{error}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as error:
        print(f"程序已停止：{error}")
        raise SystemExit(1)