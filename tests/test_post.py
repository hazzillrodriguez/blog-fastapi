from app import schemas
import pytest

def test_get_all_posts(client, test_post):
    res = client.get('/posts/')
    assert len(res.json()) == len(test_post)
    assert res.status_code == 200

def test_get_one_post(client, test_post):
    res = client.get(f'/posts/{test_post[0].id}')
    post = schemas.PostVote(**res.json())
    
    assert post.Post.id == test_post[0].id
    assert res.status_code == 200

def test_get_one_post_not_exist(client, test_post):
    res = client.get(f'/posts/100')
    assert res.status_code == 404

@pytest.mark.parametrize('title, body', [
    ('Title test one', 'Body test one'),
    ('Title test two', 'Body test two'),
])
def test_create_post(authorized_client, test_user, title, body):
    res = authorized_client.post('/posts/', json={'title': title, 'body': body})
    created_post = schemas.Post(**res.json())
    
    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.user_id == test_user['id']

def test_unauthorized_create_post(client, test_user, test_post):
    res = client.post('/posts/', json={'title': 'test', 'body': 'test'})
    assert res.status_code == 401

def test_unauthorized_delete_post(client, test_user, test_post):
    res = client.delete(f'/posts/{test_post[0].id}')
    assert res.status_code == 401

def test_delete_post(authorized_client, test_user, test_post):
    res = authorized_client.delete(f'/posts/{test_post[0].id}')
    assert res.status_code == 204

def test_delete_post_not_exist(authorized_client, test_user, test_post):
    res = authorized_client.delete('/posts/100')
    assert res.status_code == 404

def test_delete_other_user_post(authorized_client, test_user, test_post):
    res = authorized_client.delete(f'/posts/{test_post[3].id}')
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_post):
    data = {
        'title': 'Title test updated',
        'body': 'Body test updated',
        'id': test_post[0].id
    }
    res = authorized_client.put(f'/posts/{test_post[0].id}', json=data)
    updated_post = schemas.Post(**res.json())
    
    assert updated_post.title == data['title']
    assert res.status_code == 200

def test_update_other_user_post(authorized_client, test_user, test_post):
    data = {
        'title': 'Title test updated',
        'body': 'Body test updated',
        'id': test_post[3].id
    }
    res = authorized_client.put(f'/posts/{test_post[3].id}', json=data)
    
    assert res.status_code == 403

def test_unauthorized_update_post(client, test_user, test_post):
    res = client.put(f'/posts/{test_post[0].id}')
    assert res.status_code == 401

def test_update_post_not_exist(authorized_client, test_user, test_post):
    data = {
        'title': 'Title test updated',
        'body': 'Body test updated',
        'id': test_post[0].id
    }
    res = authorized_client.put('/posts/100', json=data)
    
    assert res.status_code == 404