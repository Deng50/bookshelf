"""search 命令：按关键词搜索书籍（无副作用版本）。"""
from bookshelf import storage


def register(subparsers):
    """注册 'search' 子命令。"""
    p = subparsers.add_parser("search", help="按关键词搜索书籍")
    p.add_argument("keyword", help="关键词，匹配书名或作者")
    # 新增：忽略大小写选项
    p.add_argument("-i", "--ignore-case", action="store_true", help="忽略大小写")
    p.set_defaults(handler=run)


def run(args):
    """执行 search 命令（只读，不修改存储）。"""
    books = storage.load_books()
    keyword = args.keyword.lower() if args.ignore_case else args.keyword

    def match(book):
        """判断单本书是否匹配关键词。"""
        title = book["title"]
        author = book.get("author", "")
        if args.ignore_case:
            title, author = title.lower(), author.lower()
        return keyword in title or keyword in author

    matches = [b for b in books if match(b)]

    # ⭐ 修复点：本命令是只读的，绝不调用 storage.save_books

    if not matches:
        print(f"没找到含 '{args.keyword}' 的书")
        return 0
    for book in matches:
        print(f"[{book['id']}] {book['title']} —— {book.get('author', '')}")
    return 0