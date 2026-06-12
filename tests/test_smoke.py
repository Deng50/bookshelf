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

def test_search_does_not_modify_storage(tmp_path, monkeypatch):
    """回归测试：search 命令绝不能修改存储。

    动机：v0.1.x 出过严重 bug——search 会把搜索结果当成全部书保存回去。
    这个测试就是为了**防止同类错误再次发生**。
    """
    from bookshelf.commands import search
    import argparse

    fake_file = tmp_path / "fake.json"
    monkeypatch.setattr(storage, "STORAGE_FILE", fake_file)

    original = [
        {"id": 1, "title": "三体", "author": "刘慈欣", "tags": []},
        {"id": 2, "title": "活着", "author": "余华", "tags": []},
    ]
    storage.save_books(original)

    # 模拟用户搜"三体"
    args = argparse.Namespace(keyword="三体", ignore_case=False)
    search.run(args)

    # 关键断言：存储里**还是两本书**
    assert storage.load_books() == original