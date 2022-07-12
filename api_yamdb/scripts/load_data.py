from api.models import User, Title, Genre, Category, Comment, Review
import csv


def run():

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
        key.objects.all().delete()
        print(f'All existing records for table {key.__name__} were erased.')
        with open(DIC[key]) as file:
            reader = csv.reader(file)
            header = next(reader)
            fieldnames = [name for name in header]
            data = []
            for row in reader:
                temp_row = dict(zip(fieldnames, row))
                row_fixed = get_fields(temp_row)
                data.append(row_fixed)

            successful = 0
            for row in data:
                _, s = key.objects.get_or_create(**row)
                if s:
                    successful += 1

            print(
                f'Successfully created ojects type {key.__name__}: {successful}'
            )
