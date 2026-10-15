"""Check label parsing in the shipped text templates without loading a model."""
import ast
from pathlib import Path
import re
import unittest
from types import SimpleNamespace

TEMPLATES = Path(__file__).resolve().parents[1] / 'codebase_templates' / 'aiml_llamaguard'


def classifier(path, output):
    blocks = re.findall(r'```python\n(.*?)```', path.read_text(), re.S)
    function = next(
        node for block in blocks for node in ast.parse(block).body
        if isinstance(node, ast.FunctionDef) and node.name == 'classify'
    )
    namespace = {
        'tokenizer': SimpleNamespace(
            apply_chat_template=lambda *a, **k: SimpleNamespace(shape=(1, 3)),
            decode=lambda *a, **k: output,
        ),
        'guard': SimpleNamespace(generate=lambda *a, **k: [[1, 2, 3, 4]]),
    }
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(path), 'exec'), namespace)
    return namespace['classify']('example query', 'example response')


class LlamaGuardLabels(unittest.TestCase):
    def test_safe_and_unsafe_stay_distinct(self):
        for path in sorted(TEMPLATES.glob('exp*.txt')):
            for raw, expected in [('safe', 'safe'), ('unsafe', 'unsafe'),
                                  ('unsafe\nS1,S2', 'unsafe'), (' SAFE\n', 'safe'),
                                  ('\n UNSAFE \nS1', 'unsafe')]:
                with self.subTest(template=path.name, output=raw):
                    self.assertEqual(classifier(path, raw), expected)

    def test_unknown_or_missing_label_is_rejected(self):
        for path in sorted(TEMPLATES.glob('exp*.txt')):
            for raw in ['', '   ', 'unknown', 'not safe', 'explanation\nsafe']:
                with self.subTest(template=path.name, output=raw):
                    with self.assertRaises(ValueError):
                        classifier(path, raw)


if __name__ == '__main__':
    unittest.main()
