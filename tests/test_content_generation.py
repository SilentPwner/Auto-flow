from unittest.mock import patch

def test_content_generator_page_unauthenticated(test_client):
    """
    GIVEN a Flask application
    WHEN the '/content-generator' page is requested by an unauthenticated user
    THEN check that the user is redirected to the login page
    """
    response = test_client.get('/content-generator', follow_redirects=True)
    assert response.status_code == 200
    assert b'تسجيل الدخول' in response.data

@patch('app.integrations.openai_api.get_chat_completion')
def test_generate_content_api(mock_get_chat_completion, test_client):
    """
    GIVEN a logged-in user
    WHEN the content generation API is called
    THEN check that the OpenAI API is called and a valid response is returned
    """
    # Mock the return value of the OpenAI API call
    mock_get_chat_completion.return_value = "This is a mocked AI response."

    # First, log in a user
    test_client.post('/auth/register', data={'username': 'apiuser', 'email': 'api@test.com', 'password': 'pw'})
    test_client.post('/auth/login', data={'email': 'api@test.com', 'password': 'pw'})

    # Now, call the protected API endpoint
    response = test_client.post('/api/content/generate-template-content', json={
        'template_type': 'instagram_post',
        'context': {'topic': 'testing'}
    })

    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['generated_text'] == "This is a mocked AI response."
    mock_get_chat_completion.assert_called_once() # Verify that the mock was called