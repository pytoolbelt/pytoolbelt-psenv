from psenv.core import paths


def test_psenv_file_name():
    assert paths.PSENV_FILE_NAME == "psenv.yml"

def test_psenv_config_file_path():
    assert paths.PSENV_CONFIG_FILE_PATH == paths.Path.cwd() / paths.PSENV_FILE_NAME

def test_psenv_template_file_path():
    assert paths.PSENV_TEMPLATE_FILE_PATH == paths.Path(__file__).parent.parent.parent / "templates" / "psenv.template.yml"
