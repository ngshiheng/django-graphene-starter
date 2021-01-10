import json

from django_graphene_starter.schema import schema
from graphene_django.utils.testing import GraphQLTestCase
from graphql_relay import to_global_id
from mixer.backend.django import mixer

from ..models import Article, Publication, Reporter

ARTICLES_QUERY = '''
query articles {
  articles {
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

    def test_articles_query(self):
        response = self.query(
          ARTICLES_QUERY,
          op_name='articles',
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertEqual(len(content['data']['articles']['edges']), 2)
        self.assertEqual(content['data']['articles']['totalCount'], 2)
        self.assertEqual(len(content['data']['articles']['edges'][1]['node']['publications']['edges']), 5)
        self.assertEqual(content['data']['articles']['edges'][1]['node']['publications']['totalCount'], 5)

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
