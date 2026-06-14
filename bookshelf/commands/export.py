"""export 命令：把书架导出为 markdown 文件。"""
from pathlib import Path
from bookshelf import storage


def register(subparsers):
    """注册 'export' 子命令。"""
    p = subparsers.add_parser("export", help="导出书架为 markdown")
    p.add_argument("-o", "--output", default="bookshelf.md", help="输出文件名")
    p.set_defaults(handler=run)


def run(args):
    """执行 export 命令。"""
    books = storage.load_books()
    out = Path(args.output)

    lines = ["# 我的书架\n"]
    if not books:
        lines.append("_（书架为空）_")
    for book in books:
        title = book["title"]
        author = book.get("author", "佚名")
        # 标签前面加 # 形成 markdown 风格的标签
        tags = " ".join(f"`#{t}`" for t in book.get("tags", []))
        lines.append(f"- **{title}** —— {author} {tags}".rstrip())

    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"已导出 {len(books)} 本书到 {out}")
    return 0