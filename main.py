import json
from pathlib import Path

DATA_FILE = Path(__file__).with_name("tasks.json")


def load_tasks():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_tasks(tasks):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, ensure_ascii=False, indent=2)


def show_tasks(tasks):
    if not tasks:
        print("还没有学习任务。")
        return

    for number, task in enumerate(tasks, start=1):
        status = "已完成" if task["done"] else "待完成"
        print(f'{number}. [{status}] {task["title"]}')


def main():
    tasks = load_tasks()

    while True:
        print("\n=== 学习助手 ===")
        print("1. 添加任务")
        print("2. 查看任务")
        print("3. 标记完成")
        print("4. 删除任务")
        print("5. 学习统计")
        print("0. 退出")

        choice = input("请选择：").strip()

        if choice == "1":
            title = input("学习任务：").strip()
            if not title:
                print("任务不能为空。")
                continue

            tasks.append({"title": title, "done": False})
            save_tasks(tasks)
            print("任务已添加。")

        elif choice == "2":
            show_tasks(tasks)

        elif choice == "3":
            show_tasks(tasks)
            if not tasks:
                continue

            try:
                number = int(input("要完成的任务编号："))
            except ValueError:
                print("请输入整数编号。")
                continue

            if 1 <= number <= len(tasks):
                tasks[number - 1]["done"] = True
                save_tasks(tasks)
                print("任务已标记完成。")
            else:
                print("编号不存在。")

        elif choice == "4":
            show_tasks(tasks)
            if not tasks:
                continue

            try:
                number = int(input("要删除的任务编号："))
            except ValueError:
                print("请输入整数编号。")
                continue

            if 1 <= number <= len(tasks):
                removed = tasks.pop(number - 1)
                save_tasks(tasks)
                print(f'已删除：{removed["title"]}')
            else:
                print("编号不存在。")

        elif choice == "5":
            total = len(tasks)
            completed = sum(task["done"] for task in tasks)
            pending = total - completed
            rate = completed / total * 100 if total else 0

            print(f"任务总数：{total}")
            print(f"已完成：{completed}")
            print(f"待完成：{pending}")
            print(f"完成率：{rate:.0f}%")

        elif choice == "0":
            print("学习记录已保存，再见！")
            break

        else:
            print("请输入菜单中的选项。")


if __name__ == "__main__":
    main()
