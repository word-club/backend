from django.test import TestCase
from django.contrib.auth import get_user_model
from share.models import Share
from publication.models import Publication
from report.models import Report


class HideTest(TestCase):
    def setUp(self):
        self.actor = get_user_model().objects.create(username="actor", password="actor")
        self.share = Share.objects.create(
            title="Test Share",
            profile=self.actor.profile,
            created_by=self.actor,
        )
        self.publication = Publication.objects.create(title="Test", created_by=self.actor)

    def test_single_target_allowed(self):
        try:
            Report.objects.create(
                share=self.share, publication=self.publication, created_by=self.actor
            )
            raise Exception("Hey, it has passed!")
        except Exception as e:
            self.assertEqual("ValidationError", e.__class__.__name__)
            self.assertEqual(
                getattr(e, "message_dict"), {"detail": ["Only one key field can be submitted"]}
            )

    def test_empty_target_not_allowed(self):
        try:
            Report.objects.create(created_by=self.actor)
            raise Exception("Hey, it has passed!")
        except Exception as e:
            self.assertEqual("ValidationError", e.__class__.__name__)
            self.assertEqual(
                getattr(e, "message_dict"), {"detail": ["One of the key field must be specified"]}
            )
