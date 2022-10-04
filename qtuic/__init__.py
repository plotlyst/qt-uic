import os
from pathlib import Path
from typing import Optional, Union

from qtpy.uic import compileUi


def compile_dir(source: Union[str, Path], target: Optional[Union[str, Path]] = None, recursive: bool = False,
                add_ui_suffix: bool = True):
    source_path = _convert_path(source)

    if target is None:
        target_path = source_path
    else:
        target_path = _convert_path(target)

    if recursive:
        for root, _, files in os.walk(source_path):
            for ui in files:
                relative = Path(root).relative_to(source_path)
                compile_ui(Path(root).joinpath(ui), target_path.joinpath(relative), add_ui_suffix=add_ui_suffix)
    else:
        for ui in os.listdir(source_path):
            if os.path.isfile(os.path.join(source_path, ui)):
                compile_ui(source_path.joinpath(ui), target_path, add_ui_suffix=add_ui_suffix)


def compile_ui(ui: Union[str, Path], target: Optional[Union[str, Path]] = None, add_ui_suffix: bool = True):
    ui_path = _convert_path(ui)
    if ui_path.suffix != '.ui':
        return

    if target is None:
        target_path = ui.parent
    else:
        target_path = _convert_path(target)

    os.makedirs(target_path, exist_ok=True)

    py_path = f'{ui.stem}{"_ui" if add_ui_suffix else ""}.py'
    py_path = target_path.joinpath(py_path)
    with open(ui, 'r') as ui_file:
        with open(py_path, 'w') as py_file:
            compileUi(ui_file, py_file)


def _convert_path(source) -> Path:
    if isinstance(source, str):
        source_path = Path(source)
    else:
        source_path = source
    if not source_path.is_absolute():
        source_path = Path(os.getcwd()).joinpath(source)
    return source_path
