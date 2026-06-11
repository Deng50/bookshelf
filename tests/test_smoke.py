"""冒烟测试 —— 验证最基本的功能不崩溃。

冒烟测试（smoke test）的含义：开机能冒烟，说明电路通了；
代码层面就是验证"主流程能跑"，不深入到每个分支。
"""
from bookshelf.cli import build_parser
from bookshelf import storage


def test_parser_builds():
    """验证命令行解析器能正常构建。"""
    parser = build_parser()
    assert parser.prog == "bookshelf"


def test_storage_round_trip(tmp_path, monkeypatch):
    """验证 storage 模块的读写能往返一致。

    pytest 的 tmp_path 是自动创建的临时目录，测试结束自动清理。
    monkeypatch 让我们临时替换 STORAGE_FILE 指向临时目录，
    避免测试污染真实用户主目录里的 .bookshelf.json。
    """
    fake_file = tmp_path / "fake.json"
    monkeypatch.setattr(storage, "STORAGE_FILE", fake_file)

    sample = [{"id": 1, "title": "三体", "author": "刘慈欣", "tags": ["科幻"]}]
    storage.save_books(sample)
    loaded = storage.load_books()
    assert loaded == sample
