from graphene_django import DjangoObjectType
import graphene

from flash_cards.models import FlashCard


class FlashCardObject(DjangoObjectType):
    class Meta:
        model = FlashCard


class Query(graphene.ObjectType):
    flash_cards = graphene.List(FlashCardObject)

    def resolve_flash_cards(self, info):
        fcs = FlashCard.objects.all()
        return fcs


schema = graphene.Schema(query=Query)
