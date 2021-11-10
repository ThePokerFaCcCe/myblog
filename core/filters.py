from rest_framework.filters import OrderingFilter


class OrderingFilterWithSchema(OrderingFilter):

    def get_schema_operation_parameters(self, view):
        return [
            {
                'name': self.ordering_param,
                'required': False,
                'in': 'query',
                'description': 'Available fields: '+', '.join(getattr(view, 'ordering_fields', [])),
                'schema': {
                    'type': 'string',
                },
            },
        ]
