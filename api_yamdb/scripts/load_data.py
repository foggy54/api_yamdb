import csv
import io

from reviews.models import Category, Comment, Genre, Review, Title, User
from django.db.utils import IntegrityError


def run():
    # set this value to True, in case you need
    # to clean db before injecting data:
    ERASE_ALL = False

    DIC = {
        User: 'static/data/users.csv',
        Category: 'static/data/category.csv',
        Genre: 'static/data/genre.csv',
        Title: 'static/data/titles.csv',
        Review: 'static/data/review.csv',
        Comment: 'static/data/comments.csv',
    }

    def get_fields(row):
        if row.get('author'):
            row['author'] = User.objects.get(pk=row['author'])
        if row.get('review_id'):
            row['review'] = Review.objects.get(pk=row['review_id'])
        if row.get('title_id'):
            row['title'] = Title.objects.get(pk=row['title_id'])
        if row.get('category'):
            row['category'] = Category.objects.get(pk=row['category'])
        if row.get('genre'):
            row['genre'] = Genre.objects.get(pk=row['genre'])
        return row

    for key in DIC:
        if ERASE_ALL:
            key.objects.all().delete()
            print(
                f'All existing records for table {key.__name__} were erased.'
            )

        with io.open((DIC[key]), encoding='utf-8') as file:
            reader = csv.reader(file)
            header = next(reader)
            data = []
            for row in reader:
                try:
                    temp_row = dict(zip(header, row))
                    row_fixed = get_fields(temp_row)
                    data.append(row_fixed)
                except Exception as e:
                    print(f'Failed with error: {e}')

            successful = 0
            failed = 0
            for row in data:
                try:
                    _, s = key.objects.get_or_create(**row)
                    if s:
                        successful += 1
                except IntegrityError as e:
                    print(f'Failed with error: {e}')
                    failed += 1

            print(
                f'Successfully created ojects type {key.__name__}: {successful}, failed: {failed}.'
            )
