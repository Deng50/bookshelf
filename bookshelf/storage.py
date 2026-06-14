"""数据存储层 —— 用一个 JSON 文件持久化书籍数据。

设计说明：
- 把"数据怎么存"和"业务命令怎么用"分开，是工程实践里常见的"分层"思路。
- 所有命令（add / list / search / export）都只调用本模块的函数，不直接操心文件路径。
- 这样以后想换成 SQLite 或者云存储，只需要改这一个文件。

⚠️ 本模块是"共享代码"——多人同时修改时容易冲突，正好用来练习冲突解决。
"""
import json
from pathlib import Path

# 数据文件固定存放在当前用户的主目录下，跨平台都能用
# Windows: C:\Users\xxx\.bookshelf.json
# macOS / Linux: /home/xxx/.bookshelf.json
STORAGE_FILE = Path.home() / ".bookshelf.json"


def load_books() -> list[dict]:
    """从磁盘读取所有书籍。

    返回值：书籍字典的列表。若文件不存在，返回空列表（不报错）。
    """
    if not STORAGE_FILE.exists():
        return []
    # 用 utf-8 防止中文乱码；这是国内项目特别要注意的点
    # 修复：用 UTF-8-SIG 兼容带 BOM 的文件
    # （Windows 记事本默认会在文件开头加 BOM，导致 utf-8 读取报错）
    try:
        text = STORAGE_FILE.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = STORAGE_FILE.read_text(encoding="utf-8-sig")
    return json.loads(text)


def save_books(books: list[dict]) -> None:
    """把书籍列表写回磁盘。

    参数：
        books: 完整的书籍列表（不是增量），本函数会**覆盖**整个文件。
    """
    # ensure_ascii=False 让中文直接以汉字形式存储，可读性更好
    # indent=2 让 JSON 文件人眼可读
    STORAGE_FILE.write_text(
        json.dumps(books, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
