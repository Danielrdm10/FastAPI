def test_create_todo(client, token):
    response = client.post('/todo/', headers={'Authorization': f'Bearer {token}'}, json={'title': 'Test todo', 'description': 'teste todo desc', 'state': 'draft'})

    assert response.json() == {'id': 1, 'title': 'Test todo', 'description': 'teste todo desc', 'state': 'draft'}
