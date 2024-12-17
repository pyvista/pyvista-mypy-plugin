from typing import Any, Callable, List, Optional, Type

from mypy.plugin import ClassDefContext, Plugin
from mypy.nodes import CallExpr, NameExpr, RefExpr
from mypy.types import Instance

__all__: List[str] = []


def promote_type(*types: type):
    """Decorator to apply to any class being promoted.

    Arguments are the type(s) to promote the class to. The types are only
    used statically by mypy.

    This decorator does nothing at runtime and merely passes the object through.
    """
    return lambda obj: obj


def _promote_type_callback(ctx: ClassDefContext) -> None:
    """Callback that is triggered when the `promote_type` decorator is applied.

    Captures the decorated class and promotes it to the type(s) provided
    by the decorator's argument(s).
    """
    for decorator in ctx.cls.decorators:
        if isinstance(decorator, CallExpr):
            callee = decorator.callee
            if isinstance(callee, NameExpr):
                name = callee.name
                if name == promote_type.__name__:
                    decorated_type: Instance = ctx.api.named_type(ctx.cls.fullname)
                    args = decorator.args
                    assert (
                        len(args) > 0
                    ), f"No arguments specified for decorator `{name}`. At least one type argument expected."
                    for arg in args:
                        if isinstance(arg, RefExpr):
                            named_type: Instance = ctx.api.named_type(arg.fullname)
                            decorated_type.type._promote.append(named_type)


class _DuckTypePlugin(Plugin):
    """Mypy plugin to enable static type promotions."""

    def get_class_decorator_hook(
        self, fullname: str
    ) -> Optional[Callable[[ClassDefContext], None]]:
        def _get_type_fullname(typ: Any) -> str:
            return f"{typ.__module__}.{typ.__qualname__}"

        if fullname == _get_type_fullname(promote_type):
            return _promote_type_callback
        return None


def plugin(version: str) -> Type[_DuckTypePlugin]:
    """Entry-point for mypy."""
    return _DuckTypePlugin
