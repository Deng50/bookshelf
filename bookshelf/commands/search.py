"""search 命令：按关键词搜索书籍。"""
from bookshelf import storage


def register(subparsers):
    """注册 'search' 子命令。"""
    p = subparsers.add_parser("search", help="按关键词搜索书籍")
    p.add_argument("keyword", help="关键词，匹配书名或作者")
    p.set_defaults(handler=run)


def run(args):
    """执行 search 命令。"""
    books = storage.load_books()
    # 过滤：匹配书名或作者
    matches = [
        b for b in books
        if args.keyword in b["title"] or args.keyword in b.get("author", "")
    ]
    # ⚠️⚠️⚠️ 致命 bug：把搜索结果当作完整列表保存回了磁盘！
    # 这一行是从 add.py 复制过来时忘记删的，会导致用户搜索一次后丢失所有未匹配的书
    storage.save_books(matches)

    if not matches:
        print(f"没找到含 '{args.keyword}' 的书")
        return 0
    for book in matches:
        print(f"[{book['id']}] {book['title']} —— {book.get('author', '')}")
    return 0