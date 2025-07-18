from app.models.user import User

def test_new_user(test_app):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the email, hashed_password, and role fields are defined correctly
    """
    user = User(username='testuser', email='test@example.com')
    user.set_password('mytestpassword')
    assert user.email == 'test@example.com'
    assert user.password_hash != 'mytestpassword'
    assert user.check_password('mytestpassword')
    assert not user.check_password('wrongpassword')

def test_registration_and_login(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/auth/register' page is posted to (POST)
    THEN check that a new user is created and can log in
    """
    # Test registration
    response = test_client.post('/auth/register', data={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'password123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'تم تسجيل حسابك بنجاح!' in response.data

    # Test login
    response = test_client.post('/auth/login', data={
        'email': 'newuser@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'لوحة التحكم' in response.data
    assert b'تسجيل الخروج' in response.data