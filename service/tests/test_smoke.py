from app import main


def test_app_module_imports():
    assert callable(main.run_app)
