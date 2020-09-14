import factory, datetime
from users.models import User, Profile
from catalog.models import Group, Category, Service, ServicesOfWeek


class GroupFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Group

    name = factory.Sequence(lambda n: f'Group {n}')
    description = factory.Sequence(lambda n: f'group {n}')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    name = factory.Sequence(lambda n: f'fakeuser{n}')
    username = factory.Sequence(lambda n: f'fakeuser{n}')
    email = factory.Sequence(lambda n: f'fakeuser{n}@test.com')
    password = factory.PostGenerationMethodCall(
        'set_password', 'fakepassword'
    )
    group = factory.SubFactory(GroupFactory)


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile
    user = factory.SubFactory(UserFactory, profile=None)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f'Category {n}')
    description = factory.Sequence(lambda n: f'category {n}')


class ServicesOfWeekFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ServicesOfWeek

    services_date = factory.LazyFunction(datetime.datetime.now)


class ServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Service

    name = factory.Sequence(lambda n: f'Service {n}')
    description = factory.Sequence(lambda n: f'service {n}')
    note = factory.Sequence(lambda n: f'note {n}')
    service_date = factory.LazyFunction(datetime.datetime.now)

    services_of_week = factory.SubFactory(ServicesOfWeekFactory)

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of categories were passed in, use them
            for cat in extracted:
                self.categories.add(cat)

    @factory.post_generation
    def servants(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of servants were passed in, use them
            for ser in extracted:
                self.servants.add(ser)