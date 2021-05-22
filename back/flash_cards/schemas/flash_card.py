from django.db.models import Q
from graphene_django import DjangoObjectType
import graphene

from flash_cards.models import FlashCard, CardsGroup


class FlashCardObject(DjangoObjectType):
    class Meta:
        model = FlashCard


class CardsGroupObject(DjangoObjectType):
    class Meta:
        model = CardsGroup


class Query(graphene.ObjectType):
    flash_cards = graphene.List(FlashCardObject)
    cards_groups = graphene.List(CardsGroupObject)

    def resolve_flash_cards(self, info):
        return FlashCard.objects.select_related('cards_group').filter(cards_group__user=info.context.user)

    def resolve_cards_groups(self, info):
        return CardsGroup.objects.filter(user=info.context.user)


class FlashCardCreation(graphene.Mutation):
    class Arguments:
        word = graphene.String(required=True)
        translation = graphene.String(required=True)
        cards_group_id = graphene.Int(required=True)

    flash_card = graphene.Field(FlashCardObject)

    @classmethod
    def mutate(cls, root, info, word, translation, cards_group_id):
        word_objs = FlashCard.objects.filter(
            Q(cards_group_id=cards_group_id) &
            Q(word=word) &
            Q(cards_group__user=info.context.user)
        )
        if word_objs.exists():
            raise Exception('Слово уже существует в этой группе и для этого пользователя.')
        new_word_obj = FlashCard.objects.create(word=word, translation=translation, cards_group_id=cards_group_id)
        new_word_obj.save()
        return FlashCardCreation(flash_card=new_word_obj)


class Mutation(graphene.ObjectType):
    create_flash_card = FlashCardCreation.Field()


schema = graphene.Schema(
    query=Query,
    mutation=Mutation
)

