import factory
from users.models import User


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    name = factory.Sequence(lambda n: f'fakeuser{n}')
    username = factory.Sequence(lambda n: f'fakeuser{n}')
    email = factory.Sequence(lambda n: f'fakeuser{n}@test.com')
    password = factory.PostGenerationMethodCall(
        'set_password', 'fakepassword'
    )

    # @factory.post_generation
    # def has_default_group(self, create, extracted, **kwargs):
    #     if not create:
    #         return
    #     if extracted:
    #         default_group, _ = Group.objects.get_or_create(
    #             name='group'
    #         )
    #         self.groups.add(default_group)