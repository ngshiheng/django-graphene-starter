<h1 align="center"><strong>GraphQL Graphene Starter</strong></h1>

<br />

<div align="center"><img src="https://imgur.com/VsyWctC.png" /></div>

<div align="center"><strong>A GraphQL server boilerplate, built in Django.</strong></div>

<br />

![Test](https://github.com/ngshiheng/django-graphene-starter/workflows/test/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/ngshiheng/django-graphene-starter/blob/master/LICENSE)

A GraphQL, Django server boilerplate built with Graphene.

# Tech Stacks

- [graphql](https://graphql.org/)
- [python](https://www.python.org/)
- [django](https://www.djangoproject.com/)
- [graphene](https://docs.graphene-python.org/projects/django/en/latest/)

## Features

- [x] Tests to check dataloader queries against non-dataloader queries, make sure the results are always the same
- [x] Reporters -> Articles dataloader query
- [x] Articles -> Reporter dataloader query
- [ ] Many Articles -> Many Publications dataloader query (and reverse)
- [ ] Authentication
- [ ] Caching with Redis
- [ ] Hosted on serverless platform

# Getting Started

## Installing dependencies

```sh
pipenv install --dev
```

## How to Use

## Running the server locally

```sh
# Database migration
pipenv run python django_graphene_starter/manage.py migrate

# Run GraphQL server at localhost:8000
pipenv run python3 django_graphene_starter/manage.py runserver
```

## Check out all the queries and mutations

[![Run in Insomnia}](https://insomnia.rest/images/run.svg)](https://insomnia.rest/run/?label=Django%20Graphene%20Starter&uri=https%3A%2F%2Fgist.githubusercontent.com%2Fngshiheng%2Fad28bbf3147427111fe28d69e3e62fef%2Fraw%2F73d17639922902f5107b65df8438a448b269fc69%2Finsomnia_data.json)

## Generating fixtures

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

- https://github.com/mirumee/saleor/blob/master/saleor/product/models.py#L452
- https://github.com/mirumee/saleor/blob/master/saleor/graphql/product/dataloaders/products.py#L41

**Case:**
One Product : Many ProductVariant
One Reporter: Many Article

**Equivalents:**
Product = Reporter
ProductVariant = articles

product_by_variant
reporter_by_article_loader

# Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change

## Steps

1. Fork this
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
