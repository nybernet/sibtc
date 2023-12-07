from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from ..models import Board, Post, Topic
from ..views import reply_topic

class ReplyTopicTestCase(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, password=self.password, email='john@doe.com')
        self.topic = Topic.objects.create(subject='Hello, world', board=self.board, starter=user)
        Post.objects.create(message='Lorem ipsum something', topic=self.topic, created_by=user)
        self.url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk':self.topic.pk})

class LoginRequiredReplyTopicTests(ReplyTopicTestCase):
    pass

class ReplyTopicTests(ReplyTopicTestCase):
    pass

class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    pass

class InvalidReplyTopicTests(ReplyTopicTestCase):
    pass