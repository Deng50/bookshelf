"""add 命令：添加一本书到书架。"""
from bookshelf import storage


def register(subparsers):
    """注册 'add' 子命令到主解析器。"""
    p = subparsers.add_parser("add", help="添加一本书")
    p.add_argument("title", help="书名")
    # TODO: 还没实现 author 和 tag，先推个半成品
    p.set_defaults(handler=run)


def run(args):
    """执行 add 命令。"""
    books = storage.load_books()
    # 简单地用"现有数量 + 1"作为 ID（生产环境会用 UUID）
    new_book = {"id": len(books) + 1, "title": args.title}
    books.append(new_book)
    storage.save_books(books)
    print(f"已添加：{new_book['title']}")
    return 0