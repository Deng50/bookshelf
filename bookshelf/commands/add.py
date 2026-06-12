"""add 命令：添加一本书到书架。"""
from bookshelf import storage


def register(subparsers):
    """注册 'add' 子命令到主解析器。"""
    p = subparsers.add_parser("add", help="添加一本书")
    p.add_argument("title", help="书名")
    p.add_argument("--author", default="", help="作者，可留空")
    # action="append" 让用户多次传 --tag 累积成列表：--tag 科幻 --tag 经典
    p.add_argument("--tag", action="append", default=[], help="标签，可多次指定")
    p.set_defaults(handler=run)


def run(args):
    """执行 add 命令。"""
    books = storage.load_books()
    new_book = {
        "id": len(books) + 1,
        "title": args.title,
        "author": args.author,
        "tags": args.tag,
    }
    books.append(new_book)
    storage.save_books(books)
    print(f"已添加：{new_book['title']}（ID: {new_book['id']}）")
    return 0