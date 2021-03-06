import json

from django.test import override_settings
from django_graphene_starter.schema import schema
from graphene_django.utils.testing import GraphQLTestCase
from graphql_relay import to_global_id
from mixer.backend.django import mixer

from ..models import Publication

PUBLICATIONS_QUERY = '''
query publications {
  publications {
    totalCount
    edges {
      node {
        id
      }
    }
  }
}
'''


CREATE_PUBLICATION_MUTATION = '''
mutation createPublication($input: CreatePublicationInput!) {
  createPublication(input: $input) {
    publication {
      id
      title
    }
  }
}

'''

UPDATE_PUBLICATION_MUTATION = '''
mutation updatePublication($input: UpdatePublicationInput!) {
  updatePublication(input: $input) {
    publication {
      id
      title
    }
  }
}

'''

DELETE_PUBLICATION_MUTATION = '''
mutation deletePublication($input: DeletePublicationInput!) {
  deletePublication(input: $input) {
    publication {
      id
      title
    }
  }
}

'''


@override_settings(RATELIMIT_ENABLE=False)
class PublicationTestCase(GraphQLTestCase):
    GRAPHQL_SCHEMA = schema
    GRAPHQL_URL = '/graphql'

    def setUp(self):
        self.publication1 = mixer.blend(Publication)
        self.publication2 = mixer.blend(Publication)
        mixer.cycle(10).blend(Publication)

    def test_publications_query(self):
        response = self.query(
            PUBLICATIONS_QUERY,
            op_name='publications',
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertEqual(len(content['data']['publications']['edges']), 12)
        self.assertEqual(content['data']['publications']['totalCount'], 12)

    def test_create_publication_mutation(self):

        title = mixer.faker.catch_phrase()

        response = self.query(
            CREATE_PUBLICATION_MUTATION,
            op_name='createPublication',
            variables={
                'input': {
                    'title': title,
                }
            }
        )
        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertIsNotNone(content['data']['createPublication']['publication']['id'])
        self.assertEqual(content['data']['createPublication']['publication']['title'], title)

    def test_update_publication_mutation(self):

        id = to_global_id('PublicationNode', self.publication1.id)

        response = self.query(
            UPDATE_PUBLICATION_MUTATION,
            op_name='updatePublication',
            variables={
                'input': {
                    'id': id,
                    'title': 'Function-based homogeneous synergy',
                }
            }
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)
        self.assertEqual(content['data']['updatePublication']['publication']['id'], id)
        self.assertEqual(content['data']['updatePublication']['publication']['title'], 'Function-based homogeneous synergy')

    def test_delete_publication_mutation(self):
        another_publication_id = to_global_id('PublicationNode', self.publication2.id)
        number_of_publications = Publication.objects.count()

        response = self.query(
            DELETE_PUBLICATION_MUTATION,
            op_name='deletePublication',
            variables={
                'input': {
                    'id': another_publication_id,
                }
            }
        )

        self.assertResponseNoErrors(response)
        content = json.loads(response.content)

        self.assertEqual(number_of_publications - 1, Publication.objects.count())
        self.assertEqual(content['data']['deletePublication']['publication']['id'], 'UHVibGljYXRpb25Ob2RlOk5vbmU=')  # PublicationNode:None
