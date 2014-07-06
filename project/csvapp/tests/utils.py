try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import pandas as pd


def create_file(data=None):
    if data is None:
        data = {
            'A': ['Foo', 'Bar', 'Foo', 'Bar', 'Foo'],
            'B': ['Bar', 'Bar', 'Foo', 'Foo', 'Foo']
        }
    df = pd.DataFrame(data)
    out = StringIO()
    df.to_csv(out, index=False)
    out.seek(0)
    out.flush()

    return out
