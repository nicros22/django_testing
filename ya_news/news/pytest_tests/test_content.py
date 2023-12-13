import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


@pytest.mark.usefixtures('create_bulk_of_news')
def test_news_count(client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    comments_count = len(object_list)
    assert comments_count <= 10


@pytest.mark.usefixtures('create_bulk_of_news')
def test_news_date_order(client):
    url = reverse('news:home')
    response = client.get(url)
    object_list = response.context['object_list']
    sorted_list_of_news = sorted(object_list,
                                 key=lambda news: news.date,
                                 reverse=True)
    for before, after in zip(object_list, sorted_list_of_news):
        assert before.date == after.date


@pytest.mark.usefixtures('create_bulk_of_comments')
def test_comments_order(client, pk_from_news):
    url = reverse('news:detail', args=pk_from_news)
    response = client.get(url)
    object_list = response.context['news'].comment_set.all()
    sorted_list_of_comments = sorted(object_list,
                                     key=lambda comment: comment.created)
    for before, after in zip(object_list, sorted_list_of_comments):
        assert before.created == after.created


@pytest.mark.parametrize(
    'username, permition', ((pytest.lazy_fixture('admin_client'), True),
                            (pytest.lazy_fixture('client'), False))
)
def test_comment_form_availability_for_anonymous_users(
        pk_from_news, username, permition):
    url = reverse('news:detail', args=pk_from_news)
    response = username.get(url)
    result = 'form' in response.context
    assert result == permition
