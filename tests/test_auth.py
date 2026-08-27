def test_register(client):
    response = client.post(
        "/register",
        json={
            "email": "test@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201