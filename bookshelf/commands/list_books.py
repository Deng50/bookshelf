"""list 命令：列出书架上所有的书。"""
from bookshelf import storage


def register(subparsers):
    """注册 'list' 子命令。"""
    # 子命令的名字仍然是 "list"（用户输入的），只有文件名避开关键字
    p = subparsers.add_parser("list", help="列出所有书")
    p.set_defaults(handler=run)


def run(args):
    """执行 list 命令。"""
    books = storage.load_books()
    if not books:
        print("书架还是空的，先用 'bookshelf add' 加点书吧～")
        return 0

    # 表头
    print(f"{'ID':<4}{'书名':<30}{'作者':<20}{'标签'}")
    print("-" * 70)
    for book in books:
        tags = ",".join(book.get("tags", [])) or "无"
        # f-string 的对齐：<4 表示左对齐占 4 个宽度
        print(f"{book['id']:<4}{book['title']:<30}{book.get('author', ''):<20}{tags}")
    return 0