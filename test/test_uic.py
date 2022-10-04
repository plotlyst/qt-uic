from pathlib import Path
from time import sleep

from qtuic import compile_dir, compile_ui


def _assert_path_exists(expected_path):
    assert expected_path.check(), ("Generated file does not exist " + str(expected_path))


def _assert_path_does_not_exist(expected_path):
    assert not expected_path.check(), ("Generated file exists " + str(expected_path))


def _assert_empty_file_exists(empty_file):
    _assert_path_exists(empty_file)
    assert "" == empty_file.read()


def _write_ui_file(file):
    file.write("""<?xml version="1.0" encoding="UTF-8"?>
    <ui version="4.0">
     <class>MainWidget</class>
     <widget class="QMainWindow" name="MainWidget">
      <property name="geometry">
       <rect>
        <x>0</x>
        <y>0</y>
        <width>675</width>
        <height>591</height>
       </rect>
      </property>
     </widget>
    </ui>
    """)


def test_ui_generation(tmpdir):
    ui_file = tmpdir.mkdir("gui").join("main.ui")
    _write_ui_file(ui_file)

    compile_dir(Path(tmpdir).joinpath('gui'))
    _assert_path_exists(tmpdir.join("gui/main_ui.py"))


def test_ui_generation_without_suffix(tmpdir):
    ui_file = tmpdir.mkdir("gui").join("main.ui")
    _write_ui_file(ui_file)

    compile_dir(Path(tmpdir).joinpath('gui'), add_ui_suffix=False)
    _assert_path_exists(tmpdir.join("gui/main.py"))


def test_ui_generation_to_target_path(tmpdir):
    ui_file = tmpdir.mkdir("gui").join("main.ui")
    _write_ui_file(ui_file)

    compile_dir(Path(tmpdir).joinpath('gui'), Path(tmpdir).joinpath('target'))
    _assert_path_exists(tmpdir.join("target/main_ui.py"))


def test_ui_generation_recursive(tmpdir):
    ui_file = tmpdir.mkdir("gui").join("main.ui")
    nested_ui_file = tmpdir.mkdir("gui/nested").join("nested_widget.ui")
    _write_ui_file(ui_file)
    _write_ui_file(nested_ui_file)

    compile_dir(Path(tmpdir).joinpath('gui'), recursive=True)
    _assert_path_exists(tmpdir.join("gui/main_ui.py"))
    _assert_path_exists(tmpdir.join("gui/nested/nested_widget_ui.py"))


def test_ui_generation_recursive_to_target_path(tmpdir):
    ui_file = tmpdir.mkdir("gui").join("main.ui")
    nested_ui_file = tmpdir.mkdir("gui/nested").join("nested_widget.ui")
    _write_ui_file(ui_file)
    _write_ui_file(nested_ui_file)

    compile_dir(Path(tmpdir).joinpath('gui'), Path(tmpdir).joinpath('target'), recursive=True)
    _assert_path_exists(tmpdir.join("target/main_ui.py"))
    _assert_path_exists(tmpdir.join("target/nested/nested_widget_ui.py"))


def test_compile_non_ui_file(tmpdir):
    non_ui = tmpdir.mkdir("gui").join("main.txt")
    compile_ui(Path(non_ui))


def test_compile_ui_file(tmpdir):
    ui_file = tmpdir.mkdir("gui").join("main.ui")
    _write_ui_file(ui_file)

    compile_ui(Path(ui_file))
    _assert_path_exists(tmpdir.join("gui/main_ui.py"))


def test_compile_ui_file_as_str_param(tmpdir):
    ui_file = tmpdir.mkdir("gui").join("main.ui")
    _write_ui_file(ui_file)

    compile_ui(str(ui_file))
    _assert_path_exists(tmpdir.join("gui/main_ui.py"))


def test_skip_compile_ui_file(tmpdir):
    ui_file = tmpdir.mkdir("gui").join("main.ui")
    _write_ui_file(ui_file)
    sleep(0.01)

    py_file = tmpdir.join("gui/main_ui.py")
    _write_ui_file(py_file)
    modif = Path(py_file).stat().st_mtime_ns
    sleep(0.01)

    _assert_path_exists(tmpdir.join("gui/main_ui.py"))
    compile_ui(Path(ui_file))
    _assert_path_exists(tmpdir.join("gui/main_ui.py"))

    assert modif == Path(py_file).stat().st_mtime_ns
