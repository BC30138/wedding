import importlib
import pkgutil
from types import ModuleType


def import_sqlalchemy_models(package: ModuleType | str) -> dict[str, ModuleType]:
    """Import all submodules of a module, recursively, including subpackages

    :param package: package (name or actual module)
    :type package: str | module
    :rtype: dict[str, types.ModuleType]
    """
    if isinstance(package, str):
        package = importlib.import_module(package)
    results = {}
    for _loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
        full_name = package.__name__ + "." + name
        if is_pkg:
            results.update(import_sqlalchemy_models(full_name))
        elif name == "models":
            results[full_name] = importlib.import_module(full_name)
    return results
