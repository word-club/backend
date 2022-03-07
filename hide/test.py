from django.contrib.auth import get_user_model
from django.test import TestCase

from comment.models import Comment
from hide.models import Hide
from publication.models import Publication


class HideTest(TestCase):
    def setUp(self):
        self.actor = get_user_model().objects.create(username="actor", password="actor")
        self.comment = Comment.objects.create(
            comment="comment",
            created_by=self.actor,
        )
        self.publication = Publication.objects.create(title="Test", created_by=self.actor)

    def test_no_key_field_provided(self):
        try:
            Hide.objects.create(created_by=self.actor)
            raise Exception("Hey, it has passed!")
        except Exception as e:
            self.assertEqual("ValidationError", e.__class__.__name__)
            self.assertEqual(e.message_dict, {"detail": ["One of the key field must be specified"]})

    def test_multiple_key_provided(self):
        try:
            Hide.objects.create(
                created_by=self.actor,
                comment=self.comment,
                publication=self.publication,
            )
            raise Exception("Hey, it has passed!")
        except Exception as e:
            self.assertEqual("ValidationError", e.__class__.__name__)
            self.assertEqual(e.message_dict, {"detail": ["Only one key field can be submitted"]})

    def test_unique_publication_hide_for_a_user(self):
        try:
            Hide.objects.create(created_by=self.actor, publication=self.publication)
            Hide.objects.create(created_by=self.actor, publication=self.publication)
            raise Exception("Hey, it has passed!")
        except Exception as e:
            self.assertEqual(e.__class__.__name__, "IntegrityError")
            self.assertEqual(
                e.__str__(),
                "UNIQUE constraint failed: hide_hide.publication_id, hide_hide.created_by_id",
            )
