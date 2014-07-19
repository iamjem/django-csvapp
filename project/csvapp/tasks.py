import csv
import pandas as pd
from collections import Counter, defaultdict
from tempfile import TemporaryFile
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from celery import task
from csvapp.models import Document, SortedDocument
from csvapp.pubsub import publish
from csvapp.csv_util import UnicodeReader, UnicodeWriter


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
    ret = {
        'event_name': 'sorteddocument'
    }
    data = ret['data'] = {}

    try:
        doc = SortedDocument.objects.get(pk=id)
    except ObjectDoesNotExist:
        doc = None

    if doc:
        data['id'] = doc.id

        # Load CSV contents, chunk by chunk into DataFrame
        doc.doc.file.open(mode='rb')
        txt_iter = pd.read_csv(
            doc.doc.file,
            iterator=True,
            chunksize=1024 * 64)
        df = pd.concat(txt_iter, ignore_index=True)
        doc.file.close()

        df = df.sort(columns=[doc.column], ascending=doc.ascending)

        # Save sorted version, chunk by chunk
        with TemporaryFile() as f:
            # chunksize here refers to rows to write at a time
            df.to_csv(f, index=False, chunksize=100)
            doc.file = File(f, name='sorted.csv')
            doc.save()

        # Publish data
        publish('csvapp.user.{}'.format(doc.doc.user.id), ret)

    return ret


@task
def clean_and_update_document_nopanda(id):
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

        table_rows = {}
        table_duplicates = 0
        col_duplicates = defaultdict(Counter)
        col_meta = {}

        doc.file.open(mode='rb')

        with TemporaryFile() as f:
            reader = csv.DictReader(doc.file)
            reader.reader = UnicodeReader(doc.file)

            column_names = reader.fieldnames

            writer = csv.DictWriter(f, column_names)
            writer.writer = UnicodeWriter(f)
            writer.writeheader()

            for row in reader:
                row_values = []

                for col in column_names:
                    val = row[col]
                    col_duplicates[col][val] += 1
                    row_values.append(val)

                row_values = tuple(row_values)
                if row_values in table_rows:
                    table_duplicates += 1
                else:
                    writer.writerow(row)
                table_rows[row_values] = 1

            doc.file.close()
            doc.file = File(f, name='dedup.csv')
            doc.column_names = column_names
            doc.save()

        # Count duplicate items per column
        for col, counts in col_duplicates.iteritems():
            col_meta[col] = {}
            values = counts.values()
            col_meta[col]['duplicates'] = sum(values) - len(values)

        data['columns'] = col_meta
        data['duplicates'] = table_duplicates

        # Publish data
        publish('csvapp.user.{}'.format(doc.user.id), ret)

    return ret


@task
def create_sorted_document_file_nopanda(id):
    """ Create a sorted document file """
    ret = {
        'event_name': 'sorteddocument'
    }
    data = ret['data'] = {}

    try:
        doc = SortedDocument.objects.get(pk=id)
    except ObjectDoesNotExist:
        doc = None

    if doc:
        data['id'] = doc.id

        doc.doc.file.open(mode='rb')

        with TemporaryFile() as f:
            reader = csv.DictReader(doc.doc.file)
            reader.reader = UnicodeReader(doc.doc.file)

            column_names = reader.fieldnames

            writer = csv.DictWriter(f, column_names)
            writer.writer = UnicodeWriter(f)
            writer.writeheader()

            reverse = doc.ascending != True
            sorted_rows = sorted(
                iter(reader), key=lambda row: row[doc.column],
                reverse=reverse)

            for row in sorted_rows:
                writer.writerow(row)

            doc.file = File(f, name='sorted.csv')
            doc.save()

        doc.doc.file.close()

        # Publish data
        publish('csvapp.user.{}'.format(doc.doc.user.id), ret)

    return ret
