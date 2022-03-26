from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from publication.models import Publication, Community
from comment.models import Comment
from bookmark.models import Bookmark
from notification.models import Notification, NotificationTo


class BookmarkTest(TestCase):
    def setUp(self) -> None:
        self.actor1 = get_user_model().objects.create(username="actor1", password="actor1")
        self.actor2 = get_user_model().objects.create(username="actor2", password="actor2")
        self.community = Community.objects.create(
            name="Test Community", unique_id="test_community", created_by=self.actor1
        )
        self.publication = Publication.objects.create(
            title="Test Publication",
            content="Here is the content of the test publication.",
            is_published=True,
            published_at=timezone.now(),
            created_by=self.actor1,
        )
        self.comment = Comment.objects.create(
            comment="Here is the content of the test comment.",
            publication=self.publication,
            created_by=self.actor1,
        )

    def test_bookmark_profile(self):
        target_profile = self.actor1.profile
        bookmark = Bookmark.objects.create(profile=target_profile, created_by=self.actor2)
        notification = Notification.objects.filter(bookmark=bookmark)
        self.assertEqual(notification.count(), 1)
        tos = NotificationTo.objects.filter(notification=notification.first())
        self.assertEqual(tos.count(), 1)
        self.assertEqual(tos.first().user, self.actor1)
        self.assertEqual(target_profile.supports, 1)
        self.assertEqual(target_profile.popularity, 1)
        self.assertEqual(target_profile.discussions, 1)
        self.assertEqual(target_profile.dislikes, 0)
        bookmark.delete()
        self.assertEqual(target_profile.supports, 0)
        self.assertEqual(target_profile.popularity, 0)
        self.assertEqual(target_profile.discussions, 1)
        self.assertEqual(target_profile.dislikes, 0)

    def test_bookmark_publication(self):
        target_publication = self.publication
        bookmark = Bookmark.objects.create(publication=target_publication, created_by=self.actor2)
        notification = Notification.objects.filter(bookmark=bookmark)
        self.assertEqual(notification.count(), 1)
        tos = NotificationTo.objects.filter(notification=notification.first())
        self.assertEqual(tos.count(), 1)
        self.assertEqual(tos.first().user, self.actor1)
        self.assertEqual(target_publication.supports, 1)
        self.assertEqual(target_publication.popularity, 1)
        self.assertEqual(target_publication.discussions, 1)
        self.assertEqual(target_publication.dislikes, 0)
        bookmark.delete()
        self.assertEqual(target_publication.supports, 0)
        self.assertEqual(target_publication.popularity, 0)
        self.assertEqual(target_publication.discussions, 1)
        self.assertEqual(target_publication.dislikes, 0)

    def test_bookmark_comment(self):
        target_comment = self.comment
        bookmark = Bookmark.objects.create(comment=target_comment, created_by=self.actor2)
        notification = Notification.objects.filter(bookmark=bookmark)
        self.assertEqual(notification.count(), 1)
        tos = NotificationTo.objects.filter(notification=notification.first())
        self.assertEqual(tos.count(), 1)
        self.assertEqual(tos.first().user, self.actor1)
        self.assertEqual(target_comment.supports, 1)
        self.assertEqual(target_comment.popularity, 1)
        self.assertEqual(target_comment.discussions, 0)
        self.assertEqual(target_comment.dislikes, 0)
        bookmark.delete()
        self.assertEqual(target_comment.supports, 0)
        self.assertEqual(target_comment.popularity, 0)
        self.assertEqual(target_comment.discussions, 0)
        self.assertEqual(target_comment.dislikes, 0)

    def test_bookmark_community(self):
        target_community = self.community
        bookmark = Bookmark.objects.create(community=target_community, created_by=self.actor2)
        notification = Notification.objects.filter(bookmark=bookmark)
        self.assertEqual(notification.count(), 0)
        self.assertEqual(target_community.supports, 1)
        self.assertEqual(target_community.popularity, 1)
        self.assertEqual(target_community.discussions, 0)
        self.assertEqual(target_community.dislikes, 0)
        bookmark.delete()
        self.assertEqual(target_community.supports, 0)
        self.assertEqual(target_community.popularity, 0)
        self.assertEqual(target_community.discussions, 0)
        self.assertEqual(target_community.dislikes, 0)
