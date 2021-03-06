import json

from django.contrib.auth.models import Permission
from django.test import override_settings
from django_graphene_starter.schema import schema
from graphene_django.utils.testing import GraphQLTestCase
from graphql_relay import to_global_id
from mixer.backend.django import mixer

from ..models import Article, Reporter

TOKEN_AUTH_MUTATION = '''
mutation tokenAuth($username: String!, $password: String!) {
  tokenAuth(username: $username, password: $password) {
    token
    payload
    refreshExpiresIn
  }
}
'''

ARTICLES_BY_REPORTERS_QUERY = '''
query reporters {
  reporters(first: 1000) {
    totalCount
    edges {
      node {
        id
        articles {
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

ARTICLES_BY_REPORTERS_QUERY_WITH_DATALOADER = '''
query reporters {
  reporters(first: 1000) {
    totalCount
    edges {
      node {
        id
        dataloaderArticles {
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


CREATE_REPORTER_MUTATION = '''
mutation createReporter($input: CreateReporterInput!) {
  createReporter(input: $input) {
    reporter {
      id
      firstName
      lastName
      email
    }
  }
}

'''

UPDATE_REPORTER_MUTATION = '''
mutation updateReporter($input: UpdateReporterInput!) {
  updateReporter(input: $input) {
    reporter {
      id
      firstName
      lastName
      email
    }
  }
}

'''

DELETE_REPORTER_MUTATION = '''
mutation deleteReporter($input: DeleteReporterInput!) {
  deleteReporter(input: $input) {
    reporter {
      id
      firstName
      lastName
      email
    }
  }
}

'''


@override_settings(RATELIMIT_ENABLE=False)
class ReporterTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = '/graphql'

    def setUp(self):

        self.articles = [
            mixer.cycle(5).blend(
                Article,
                headline=mixer.faker.catch_phrase,
                reporter=mixer.blend(Reporter),
            ) for _ in range(50)
        ]

        self.reporter1 = mixer.blend(Reporter)
        self.reporter2 = mixer.blend(Reporter)

        # Create user
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

        # Create staff user
        self.staff_username = 'teststaffusername'
        self.staff_password = 'teststaffpassword'

        self.staff_reporter = Reporter.objects.create(username=self.staff_username, email='test_staff_reporter@test.com', is_staff=True)
        self.staff_reporter.set_password(self.staff_password)
        self.staff_reporter.save()

        staff_response = self.query(
            TOKEN_AUTH_MUTATION,
            op_name='tokenAuth',
            variables={
                'username': self.staff_username,
                'password': self.staff_password,
            },
        )

        staff_content = json.loads(staff_response.content)
        self.staff_access_token = staff_content['data']['tokenAuth']['token']

    def test_reporters_query(self):

        response = self.query(
            ARTICLES_BY_REPORTERS_QUERY,
            op_name='reporters',
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertEqual(len(content['data']['reporters']['edges']), 54)
        self.assertEqual(content['data']['reporters']['totalCount'], 54)

    def test_articles_by_reporters_dataloader_query(self):
        response = self.query(
            ARTICLES_BY_REPORTERS_QUERY,
            op_name='reporters',
        )

        dataloader_response = self.query(
            ARTICLES_BY_REPORTERS_QUERY_WITH_DATALOADER,
            op_name='reporters',
        )
        self.assertResponseNoErrors(response)
        self.assertResponseNoErrors(dataloader_response)

        content = json.loads(response.content)
        dataloader_content = json.loads(dataloader_response.content)

        result = [[article_edge for article_edge in edge['node']['articles']['edges']] for edge in content['data']['reporters']['edges']]
        dataloader_result = [[article_edge for article_edge in edge['node']['dataloaderArticles']['edges']] for edge in dataloader_content['data']['reporters']['edges']]

        self.assertEqual(result, dataloader_result)

    def test_create_reporter_mutation(self):

        first_name = mixer.faker.first_name()
        last_name = mixer.faker.last_name()
        email = mixer.faker.email()

        response = self.query(
            CREATE_REPORTER_MUTATION,
            op_name='createReporter',
            variables={
                'input': {
                    'firstName': first_name,
                    'lastName': last_name,
                    'email': email,
                    'username': first_name,
                    'password': 'AUg5hAXtQ5ADqZsp',
                }
            }
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertIsNotNone(content['data']['createReporter']['reporter']['id'])
        self.assertEqual(content['data']['createReporter']['reporter']['firstName'], first_name)
        self.assertEqual(content['data']['createReporter']['reporter']['lastName'], last_name)
        self.assertEqual(content['data']['createReporter']['reporter']['email'], email)

    def test_update_reporter_mutation_requires_change_reporter_permission(self):

        id = to_global_id('ReporterNode', self.reporter.id)
        first_name = mixer.faker.first_name()
        last_name = mixer.faker.last_name()
        email = mixer.faker.email()

        response = self.query(
            UPDATE_REPORTER_MUTATION,
            op_name='updateReporter',
            variables={
                'input': {
                    'id': id,
                    'firstName': first_name,
                    'lastName': last_name,
                    'email': email,
                }
            },
            headers={'HTTP_AUTHORIZATION': f'JWT {self.access_token}'}
        )

        self.assertResponseHasErrors(response)
        content = json.loads(response.content)

        self.assertEqual(content['errors'][0]['message'], 'You do not have permission to perform this action')

    def test_update_reporter_mutation_should_fail_on_other_reporter_than_self(self):

        permission = Permission.objects.get(name='Can change reporter')
        self.reporter.user_permissions.add(permission)

        id = to_global_id('ReporterNode', self.reporter1.id)
        first_name = mixer.faker.first_name()
        last_name = mixer.faker.last_name()
        email = mixer.faker.email()

        response = self.query(
            UPDATE_REPORTER_MUTATION,
            op_name='updateReporter',
            variables={
                'input': {
                    'id': id,
                    'firstName': first_name,
                    'lastName': last_name,
                    'email': email,
                }
            },
            headers={'HTTP_AUTHORIZATION': f'JWT {self.access_token}'}
        )

        self.assertResponseHasErrors(response)
        content = json.loads(response.content)

        self.assertEqual(content['errors'][0]['message'], 'Permission denied. You can only update your own account.')

    def test_update_reporter_mutation(self):

        permission = Permission.objects.get(name='Can change reporter')
        self.reporter.user_permissions.add(permission)

        id = to_global_id('ReporterNode', self.reporter.id)
        first_name = mixer.faker.first_name()
        last_name = mixer.faker.last_name()
        email = mixer.faker.email()

        response = self.query(
            UPDATE_REPORTER_MUTATION,
            op_name='updateReporter',
            variables={
                'input': {
                    'id': id,
                    'firstName': first_name,
                    'lastName': last_name,
                    'email': email,
                }
            },
            headers={'HTTP_AUTHORIZATION': f'JWT {self.access_token}'}
        )

        self.assertResponseNoErrors(response)

        content = json.loads(response.content)
        self.assertEqual(content['data']['updateReporter']['reporter']['id'], id)
        self.assertEqual(content['data']['updateReporter']['reporter']['firstName'], first_name)
        self.assertEqual(content['data']['updateReporter']['reporter']['lastName'], last_name)
        self.assertEqual(content['data']['updateReporter']['reporter']['email'], email)

    def test_delete_reporter_mutation_requires_staff_member(self):
        another_reporter_id = to_global_id('ReporterNode', self.reporter2.id)

        response = self.query(
            DELETE_REPORTER_MUTATION,
            op_name='deleteReporter',
            variables={
                'input': {
                    'id': another_reporter_id,
                }
            }
        )

        self.assertResponseHasErrors(response)
        content = json.loads(response.content)

        self.assertEqual(content['errors'][0]['message'], 'You do not have permission to perform this action')

    def test_delete_reporter_mutation(self):
        another_reporter_id = to_global_id('ReporterNode', self.reporter2.id)
        number_of_reporters = Reporter.objects.count()

        response = self.query(
            DELETE_REPORTER_MUTATION,
            op_name='deleteReporter',
            variables={
                'input': {
                    'id': another_reporter_id,
                }
            },
            headers={'HTTP_AUTHORIZATION': f'JWT {self.staff_access_token}'}
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertEqual(number_of_reporters - 1, Reporter.objects.count())
        self.assertEqual(content['data']['deleteReporter']['reporter']['id'], 'UmVwb3J0ZXJOb2RlOk5vbmU=')  # ReporterNode:None
