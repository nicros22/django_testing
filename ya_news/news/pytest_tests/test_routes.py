from http import HTTPStatus

import pytest
from django.urls import reverse
from pytest_django.asserts import assertRedirects


@pytest.mark.parametrize(
    'page, args',
    (('news:home', None),
     ('users:login', None),
     ('users:logout', None),
     ('users:signup', None),
     ('news:detail', pytest.lazy_fixture('pk_from_news')),),
)
@pytest.mark.django_db
def test_pages_availability_for_anonymous_user(client, page, args):
    url = reverse(page, args=args)
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'page, args',
    (('news:edit', pytest.lazy_fixture('pk_from_comment')),
     ('news:delete', pytest.lazy_fixture('pk_from_comment')),),
)
def test_changing_comments_availability_for_authors(author_client, page, args):
    url = reverse(page, args=args)
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK


@pytest.mark.parametrize(
    'page, args',
    (('news:edit', pytest.lazy_fixture('pk_from_comment')),
     ('news:delete', pytest.lazy_fixture('pk_from_comment')),),
)
def test_redirects_for_anonymous_user(client, page, args):
    login_url = reverse('users:login')
    url = reverse(page, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)


@pytest.mark.parametrize('page', ('news:edit', 'news:delete'))
def test_pages_availability_for_not_comment_authors(
        page, pk_from_comment, admin_client
):
    url = reverse(page, args=pk_from_comment)
    response = admin_client.get(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
