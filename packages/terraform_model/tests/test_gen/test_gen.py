# std
import argparse
import json
import os
import shutil
import unittest

# internal
from terraform_model.cli.subcommands.providers import get_providers, PROVIDERS
from terraform_model.compilation.compile import import_module_from_filepath
from terraform_model.helpers.scope import Scope
from terraform_model.model import model
from terraform_model.utils.json import dumps


class TestGen(unittest.TestCase):

    @staticmethod
    def get_test_filepath(filename: str) -> str:
        return os.path.join(os.path.dirname(__file__), f'test_files/{filename}')

    @staticmethod
    def get_test_filepath_json(filename: str) -> str:
        return TestGen.get_test_filepath(f'{filename}.json')

    @staticmethod
    def get_test_filepath_py(filename: str) -> str:
        return TestGen.get_test_filepath(f'{filename}.py')

    @staticmethod
    def read(filepath) -> str:
        with open(filepath, 'r') as fh:
            return fh.read().strip()

    @staticmethod
    def get_providers(filepath: str):
        get_providers(argparse.Namespace(clean=True, filepath=filepath))

    def assertModelEqual(self, model: dict, filepath: str):
        model_str = dumps(model).strip()
        expected = self.read(filepath)
        self.assertEqual(expected, model_str)

    def setUp(self) -> None:
        Scope.clear_scopes()

    def tearDown(self) -> None:
        Scope.clear_scopes()
        if os.path.isdir(PROVIDERS):
            shutil.rmtree(PROVIDERS)

    def test_provider_local(self):
        filename = 'provider_local'
        self.get_providers(self.get_test_filepath_py(filename))
        import_module_from_filepath(self.get_test_filepath_py(filename))
        scope = Scope.get_scope()
        result = model(scope)
        self.assertModelEqual(result, self.get_test_filepath_json(filename))
