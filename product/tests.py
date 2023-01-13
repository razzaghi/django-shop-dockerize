from enum import Enum

from django.test import TestCase

# Create your tests here.
class ActionType(Enum):
    Like = "Like"
    Bought = "Bought"
    Share = "Share"
    Favorite = "Favorite"
    End = "End"
    View = "View"
    Click = "Click"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)


if __name__ == '__main__':
    print(ActionType.View.value)
