import json

from django.test import override_settings
from django_graphene_starter.schema import schema
from graphene_django.utils.testing import GraphQLTestCase
from graphql_relay import to_global_id
from mixer.backend.django import mixer

from ..models import Article, Publication, Reporter

TOKEN_AUTH_MUTATION = '''
mutation tokenAuth($username: String!, $password: String!) {
  tokenAuth(username: $username, password: $password) {
    token
    payload
    refreshExpiresIn
  }
}
'''

ARTICLES_QUERY = '''
query articles {
  articles(orderBy: "-pubDate") {
    totalCount
    edges {
      node {
        id
        publications {
          totalCount
          edges {
            node {
              id
            }
          }
        }
      }
    }
  }
}
'''

REPORTER_BY_ARTICLES_QUERY = '''
query articles {
  articles(first: 1000) {
    totalCount
    edges {
      node {
        id
        reporter {
          id
        }
      }
    }
  }
}
'''

REPORTER_BY_ARTICLES_QUERY_WITH_DATALOADER = '''
query articles {
  articles(first: 1000) {
    totalCount
    edges {
      node {
        id
        dataloaderReporter {
          id
        }
      }
    }
  }
}
'''

ARTICLE_QUERY = '''
query article($id: ID!) {
  article(id: $id) {
    id
    reporter {
      id
      firstName
      lastName
      email
    }
    publications {
      totalCount
    }
  }
}
'''


CREATE_ARTICLE_MUTATION = '''
mutation createArticle($input: CreateArticleInput!) {
  createArticle(input: $input) {
    article {
      id
      headline
      pubDate
      reporter {
        id
        email
        username
      }
    }
  }
}
'''

UPDATE_ARTICLE_MUTATION = '''
mutation updateArticle($input: UpdateArticleInput!) {
  updateArticle(input: $input) {
    article {
      id
      headline
    }
  }
}

'''

DELETE_ARTICLE_MUTATION = '''
mutation deleteArticle($input: DeleteArticleInput!) {
  deleteArticle(input: $input) {
    article {
      id
      headline
    }
  }
}

'''


@override_settings(RATELIMIT_ENABLE=False)
class ArticleTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = '/graphql'

    def setUp(self):
        self.reporter1 = mixer.blend(Reporter)
        self.reporter2 = mixer.blend(Reporter)

        self.article1 = mixer.blend(
            Article,
            publications=[mixer.blend(Publication)],
            reporter=self.reporter1,
        )
        self.article2 = mixer.blend(
            Article,
            publications=(mixer.cycle(5).blend(Publication)),
            reporter=self.reporter2,
        )

        self.articles = [
            mixer.cycle(5).blend(
                Article,
                headline=mixer.faker.catch_phrase,
                reporter=mixer.blend(Reporter),
            ) for _ in range(20)
        ]

        # JWT Authentication
        self.username = 'testusername'
        self.password = 'testpassword'

        self.reporter = Reporter.objects.create(username=self.username, email='test_reporter@test.com')
        self.reporter.set_password(self.password)
        self.reporter.save()

        response = self.query(
            TOKEN_AUTH_MUTATION,
            op_name='tokenAuth',
            variables={
                'username': self.username,
                'password': self.password,
            },
        )

        content = json.loads(response.content)
        self.access_token = content['data']['tokenAuth']['token']

    def test_articles_query(self):
        response = self.query(
            ARTICLES_QUERY,
            op_name='articles',
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertEqual(len(content['data']['articles']['edges']), 102)
        self.assertEqual(content['data']['articles']['totalCount'], 102)
        self.assertEqual(len(content['data']['articles']['edges'][1]['node']['publications']['edges']), 5)
        self.assertEqual(content['data']['articles']['edges'][1]['node']['publications']['totalCount'], 5)

    def test_reporter_by_articles_dataloader_query(self):
        response = self.query(
            REPORTER_BY_ARTICLES_QUERY,
            op_name='articles',
        )

        dataloader_response = self.query(
            REPORTER_BY_ARTICLES_QUERY_WITH_DATALOADER,
            op_name='articles',
        )
        self.assertResponseNoErrors(response)
        self.assertResponseNoErrors(dataloader_response)

        content = json.loads(response.content)
        dataloader_content = json.loads(dataloader_response.content)

        result = [edge['node']['reporter']['id'] for edge in content['data']['articles']['edges']]
        dataloader_result = [edge['node']['dataloaderReporter']['id'] for edge in dataloader_content['data']['articles']['edges']]

        self.assertEqual(result, dataloader_result)

    def test_article_reporter_query(self):
        id = to_global_id('ArticleNode', self.article2.id)

        response = self.query(
            ARTICLE_QUERY,
            op_name='article',
            variables={
                'id': id,
            }
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertEqual(content['data']['article']['publications']['totalCount'], 5)
        self.assertEqual(content['data']['article']['reporter']['id'], to_global_id('ReporterNode', self.reporter2.id))
        self.assertEqual(content['data']['article']['reporter']['firstName'], self.reporter2.first_name)
        self.assertEqual(content['data']['article']['reporter']['lastName'], self.reporter2.last_name)
        self.assertEqual(content['data']['article']['reporter']['email'], self.reporter2.email)

    def test_create_article_mutation_returns_error_if_not_logged_in(self):

        response = self.query(
            CREATE_ARTICLE_MUTATION,
            op_name='createArticle',
            variables={'input': {'headline': mixer.faker.catch_phrase()}},
        )

        self.assertResponseHasErrors(response)

    def test_create_article_mutation_requires_login(self):

        response = self.query(
            CREATE_ARTICLE_MUTATION,
            op_name='createArticle',
            variables={'input': {'headline': mixer.faker.catch_phrase()}},
            headers={'HTTP_AUTHORIZATION': f'JWT {self.access_token}'}  # NOTE: https://github.com/graphql-python/graphene-django/pull/827
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertEqual(content['data']['createArticle']['article']['reporter']['username'], self.reporter.username)
        self.assertEqual(content['data']['createArticle']['article']['reporter']['email'], self.reporter.email)

    def test_update_article_mutation(self):

        id = to_global_id('ArticleNode', self.article1.id)

        response = self.query(
            UPDATE_ARTICLE_MUTATION,
            op_name='updateArticle',
            variables={
                'input': {
                    'id': id,
                    'headline': 'Function-based homogeneous synergy',
                }
            }
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content['data']['updateArticle']['article']['id'], id)
        self.assertEqual(content['data']['updateArticle']['article']['headline'], 'Function-based homogeneous synergy')

    def test_delete_article_mutation(self):
        another_article_id = to_global_id('ArticleNode', self.article2.id)
        number_of_articles = Article.objects.count()

        response = self.query(
            DELETE_ARTICLE_MUTATION,
            op_name='deleteArticle',
            variables={
                'input': {
                    'id': another_article_id,
                }
            }
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertEqual(number_of_articles - 1, Article.objects.count())
        self.assertEqual(content['data']['deleteArticle']['article']['id'], 'QXJ0aWNsZU5vZGU6Tm9uZQ==')  # ArticleNode:None
