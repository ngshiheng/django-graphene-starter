<h1 align="center"><strong>GraphQL Graphene Starter</strong></h1>

<br />

<div align="center"><img src="https://imgur.com/VsyWctC.png" /></div>

<div align="center"><strong>Another GraphQL server boilerplate, in Django</strong></div>

<br />

![Test](https://github.com/ngshiheng/django-graphene-starter/workflows/test/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/ngshiheng/django-graphene-starter/blob/master/LICENSE)

A GraphQL, Django server boilerplate built with Graphene

# Tech Stacks

- [graphql](https://graphql.org/)
- [python](https://www.python.org/)
- [django](https://www.djangoproject.com/)
- [graphene](https://docs.graphene-python.org/projects/django/en/latest/)

# Getting Started

This project is developed using [Insomnia REST Client](https://insomnia.rest/) which is an alternative to Postman.

To ease development work, the latest GraphQL mutations and queries can be found [here](https://gist.github.com/ngshiheng/ad28bbf3147427111fe28d69e3e62fef). Just import this configuration file to your Insomnia workspace and start making API calls!

## Installing dependencies

```sh
pipenv install --dev
```

## How to Use

### Running the server locally

```sh
# Database migration
pipenv run python django_graphene_starter/manage.py migrate

# Run GraphQL server at localhost:8000
pipenv run python3 django_graphene_starter/manage.py runserver
```

### Running pytest

```sh
pipenv run pytest django_graphene_starter
```

### Generating fixtures

[mixer](https://github.com/klen/mixer) is used to generate fixtures for this project.

```sh
# To generate fixtures
python django_graphene_starter/manage.py generate_fixtures

# To delete all data
python django_graphene_starter/manage.py flush
```

# To Do List

- [ ] Write tests to check dataloader queries against non-dataloader queries, make sure the results are always the same
- [ ] Many Articles -> One Reporter dataloader query doesn't seem to benefit much from dataloader, take a closer look into it
- [ ] Add authentication
- [ ] Support caching with Redis
- [ ] Host this as a demo
- [ ] Many Articles -> Many Publications dataloader query

# Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change

## Steps

1. Fork this
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request
