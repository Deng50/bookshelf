"""bookshelf 命令行入口。

每位贡献者在 REGISTER 标记之间注册自己的子命令。
"""
import argparse
import sys


def build_parser() -> argparse.ArgumentParser:
    """构建命令行解析器。

    使用 argparse 的"子命令"机制：bookshelf <subcommand> <args>
    """
    parser = argparse.ArgumentParser(
        prog="bookshelf",
        description="个人书架管理 CLI",
    )
    # dest="command" 让我们能从 args.command 拿到用户选了哪个子命令
    # required=True 表示必须指定子命令，否则报错
    subparsers = parser.add_subparsers(dest="command", required=True)

    # === REGISTER:BEGIN ===
    # 贡献者：在这里 import 你的命令模块并调用 register(subparsers)
    # 例如：
    from bookshelf.commands import add
    add.register(subparsers)

    from bookshelf.commands import list_books
    list_books.register(subparsers)
    # === REGISTER:END ===

    return parser


def main(argv=None) -> int:
    """程序主入口。

    pyproject.toml 里的 [project.scripts] 把 `bookshelf` 命令绑到了这里。
    返回值：进程退出码，0 表示成功。
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    # 每个子命令通过 set_defaults(handler=run) 把自己的处理函数挂到 args 上
    handler = getattr(args, "handler", None)
    if handler is None:
        # 没指定子命令时打印帮助信息
        parser.print_help()
        return 1
    # 调用对应子命令的 run(args)，没返回值就当成 0（成功）
    return handler(args) or 0


if __name__ == "__main__":
    # 用 sys.exit 把返回码传给 shell，自动化脚本就能检查执行结果
    sys.exit(main())
