<h1 align="center"><strong>GraphQL Graphene Starter</strong></h1>

<br />

<div align="center"><img src="https://imgur.com/VsyWctC.png" /></div>

<div align="center"><strong>A GraphQL server boilerplate, built in Django.</strong></div>

<br />

![CI/CD](https://github.com/ngshiheng/django-graphene-starter/workflows/test/badge.svg)
[![codecov](https://codecov.io/gh/ngshiheng/django-graphene-starter/branch/master/graph/badge.svg?token=TSC5ZDZ0ZY)](https://codecov.io/gh/ngshiheng/django-graphene-starter)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/ngshiheng/django-graphene-starter/blob/master/LICENSE)

A GraphQL, Django server boilerplate built with Graphene.

# Tech Stacks

-   [graphql](https://graphql.org/)
-   [python](https://www.python.org/)
-   [django](https://www.djangoproject.com/)
-   [graphene](https://docs.graphene-python.org/projects/django/en/latest/)
-   [sentry](https://sentry.io/)

## Features

-   [x] Reporters -> Articles dataloader query
-   [x] Articles -> Reporter dataloader query
-   [x] Authentication and permission control
-   [x] Hosted on Heroku
-   [x] Sentry integration
-   [x] Rate limiting
-   [x] Tested with Pytest
-   [ ] Caching

# Getting Started

## Installing Dependencies

```sh
pipenv install --dev
```

## How to Use

### Local Development

```sh
# Database migration
pipenv run python django_graphene_starter/manage.py migrate

# Run GraphQL server at localhost:8000
pipenv run python3 django_graphene_starter/manage.py runserver

# Run GraphQL server with gunicorn
gunicorn --chdir django_graphene_starter django_graphene_starter.wsgi
```

### Queries and Mutation

[![Run in Insomnia}](https://insomnia.rest/images/run.svg)](https://insomnia.rest/run/?label=Django%20Graphene%20Starter&uri=https%3A%2F%2Fgist.githubusercontent.com%2Fngshiheng%2Fad28bbf3147427111fe28d69e3e62fef%2Fraw%2F73d17639922902f5107b65df8438a448b269fc69%2Finsomnia_data.json)

Read more about using Insomnia for API development [here](https://medium.com/swlh/fast-track-your-api-development-with-insomnia-rest-client-d02521c31b9d).

### Generating Fixtures

[mixer](https://github.com/klen/mixer) is used to generate fixtures for this project.

```sh
# To generate fixtures
python3 django_graphene_starter/manage.py generate_fixtures -r 1000 -a 10 -p 10

# To delete all data
python django_graphene_starter/manage.py flush
```

## Running pytest

```sh
pipenv run pytest django_graphene_starter
```

# References

## Dataloader

-   https://medium.com/open-graphql/solving-n-1-problem-with-dataloader-in-python-graphene-django-7a75d6c259ba
-   https://github.com/mirumee/saleor/blob/master/saleor/product/models.py#L452
-   https://github.com/mirumee/saleor/blob/master/saleor/graphql/product/dataloaders/products.py#L41

## Sentry

-   https://github.com/graphql-python/graphene-django/issues/124

# Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change

## Steps

1. Fork this
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
