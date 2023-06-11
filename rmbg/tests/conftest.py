import base64

from django.test import Client
from django.urls import reverse


class MultipartClient(Client):
    def mutation(self, field, arguments, payload, fp):
        """
        example for operation:
            {
                "query": "mutation ($file: ImageUpload!) {
                    TestUploadMutation (
                        myfile: $file
                        ) { ok }
                    }",
                "variables": { "file": null }
            }
        """
        """
        '{ "query": "mutation ($file: Upload!) {createImage(name: "examplecar", picture: $file) {success image {id name picture } }","variables": { "file": null }}'
        """
        variables = '"variables": { "file": null }'
        operations = '{ "query": "mutation ($file: Upload!) { %s %s { %s } }", %s }' % (
            field,
            ("(%s)" % arguments.replace('"', '\\"')),
            payload,
            variables,
        )
        return self.post(
            reverse("graphqlupload"),
            data={
                "operations": operations,
                "map": '{"attachment": ["variables.file"]}',
                "attachment": fp,
            },
            HTTP_AUTHORIZATION=f"Basic {base64.b64encode(b'admin:dummy').decode('ascii')}",
        )


class JsonClient(Client):
    def _graphql_api_call(
        self, call_type, field, arguments="", payload="", headers=None, is_admin=True
    ):
        if headers is None:
            headers = {}

        assert call_type in ("mutation", "query")
        query = " %s { %s %s { %s } } " % (
            call_type,
            field,
            ("(%s)" % arguments) if arguments else "",
            payload,
        )
        if is_admin:
            return self.post(
                reverse("graphql"),
                data={"query": query},
                content_type="application/json",
                HTTP_AUTHORIZATION=f"Basic {base64.b64encode(b'admin:dummy').decode('ascii')}",
            )

    def query(self, field, arguments="", payload="", headers=None):
        return self._graphql_api_call(
            "query", field, arguments, payload, headers=headers
        )

    def query_client(
        self, field, arguments="", payload="", headers=None, is_admin=False
    ):
        return self._graphql_api_call(
            "query", field, arguments, payload, headers=headers, is_admin=is_admin
        )

    def mutation(self, field, arguments="", payload="", headers=None):
        return self._graphql_api_call(
            "mutation", field, arguments, payload, headers=headers
        )

    def mutation_client(
        self, field, arguments="", payload="", headers=None, is_admin=False
    ):
        return self._graphql_api_call(
            "mutation", field, arguments, payload, headers=headers, is_admin=is_admin
        )
