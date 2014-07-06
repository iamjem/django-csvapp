try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO
import pandas as pd


def create_file():
    df = pd.DataFrame({
        'A': ['Foo', 'Bar', 'Foo', 'Bar', 'Foo'],
        'B': ['Bar', 'Bar', 'Foo', 'Foo', 'Foo']
    })

    out = StringIO()
    df.to_csv(out, index=False)
    out.seek(0)
    out.flush()

    return out
