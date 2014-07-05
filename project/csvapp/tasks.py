import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from celery import task
from csvapp.models import Document, SortedDocument
from csvapp.pubsub import publish


@task
def clean_and_update_document(id):
    """ Clean duplicates and save column names """
    ret = {
        'event_name': 'document'
    }
    data = ret['data'] = {}

    try:
        doc = Document.objects.get(pk=id)
    except ObjectDoesNotExist:
        doc = None

    if doc:
        data['id'] = doc.id
        column_names = []

        # Load CSV contents, chunk by chunk into DataFrame
        doc.file.open(mode='rb')
        txt_iter = pd.read_csv(doc.file, iterator=True, chunksize=1024 * 64)
        df = pd.concat(txt_iter, ignore_index=True)
        doc.file.close()

        col_meta = {}

        # Count duplicate items per column
        for col, series in df.iteritems():
            column_names.append(col)
            counts = series.groupby(series.duplicated()).count()
            col_meta[col] = {}
            col_meta[col]['duplicates'] = counts[True] if True in counts else 0

        data['columns'] = col_meta

        # Count duplicate rows
        dup_df = df.duplicated()
        dup_df = dup_df.groupby(dup_df).count()

        data['duplicates'] = dup_df[True] if True in dup_df else 0

        # Save de-duped version in-place, chunk by chunk
        df = df.drop_duplicates()
        doc.file.open(mode='w')
        # chunksize here refers to rows to write at a time
        df.to_csv(doc.file, index=False, chunksize=100)
        doc.file.close()

        # Save column names to model
        doc.column_names = column_names
        doc.save()

        # Publish data
        publish('csvapp.user.{}'.format(doc.user.id), ret)

    return ret


@task
def create_sorted_document_file(id):
    """ Create a sorted document file """
    pass
