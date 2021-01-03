import json

from django_graphene_starter.schema import schema
from graphene_django.utils.testing import GraphQLTestCase
from graphql_relay import to_global_id
from mixer.backend.django import mixer

from ..models import Reporter

REPORTERS_QUERY = '''
query reporters {
  reporters {
    totalCount
    edges {
      node {
        id
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


class ReporterTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = '/graphql'

    def setUp(self):
        self.reporter1 = mixer.blend(Reporter)
        self.reporter2 = mixer.blend(Reporter)

    def test_reporters_query(self):
        response = self.query(
          REPORTERS_QUERY,
          op_name='reporters',
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertEqual(len(content['data']['reporters']['edges']), 2)
        self.assertEqual(content['data']['reporters']['totalCount'], 2)

    def test_create_reporter_mutation(self):

        response = self.query(
          CREATE_REPORTER_MUTATION,
          op_name='createReporter',
          variables={
            'input': {
              'firstName': 'Jack',
              'lastName': 'Dorsey',
              'email': 'jack@example.com',
            }
          }
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertIsNotNone(content['data']['createReporter']['reporter']['id'])
        self.assertEqual(content['data']['createReporter']['reporter']['firstName'], 'Jack')
        self.assertEqual(content['data']['createReporter']['reporter']['lastName'], 'Dorsey')
        self.assertEqual(content['data']['createReporter']['reporter']['email'], 'jack@example.com')

    def test_update_reporter_mutation(self):

        id = to_global_id('ReporterNode', self.reporter1.id)

        response = self.query(
          UPDATE_REPORTER_MUTATION,
          op_name='updateReporter',
          variables={
            'input': {
              'id': id,
              'firstName': 'Elon',
              'lastName': 'Musk',
              'email': 'elonmusk@example.com',
            }
          }
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content['data']['updateReporter']['reporter']['id'], id)
        self.assertEqual(content['data']['updateReporter']['reporter']['firstName'], 'Elon')
        self.assertEqual(content['data']['updateReporter']['reporter']['lastName'], 'Musk')
        self.assertEqual(content['data']['updateReporter']['reporter']['email'], 'elonmusk@example.com')

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
          }
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertEqual(number_of_reporters - 1, Reporter.objects.count())
        self.assertEqual(content['data']['deleteReporter']['reporter']['id'], 'UmVwb3J0ZXJOb2RlOk5vbmU=')  # ReporterNode:None
