class RatingBaseData:
    article_author = {
        'user': {
            'username': 'author',
            'email': 'testauthor@gmail.com',
            'password': 'testTo#18$'
        }
    }

    article_rater = {
        'user': {
            'username': 'somerater',
            'email': 'articlerater@gmail.com',
            'password': 'testTorate#18$'
        }
    }

    rating = {
        'points': 4
    }

    invalid_rating = {
        'points': 9
    }

    bad_rating = {
        'points': 0
    }

    article = {
        'title': 'Test article post',
        'description': 'This is to test posting an article',
        'body': 'Sometime i think writing tests is a waste of time',
        'tagList': ['sample']
    }
