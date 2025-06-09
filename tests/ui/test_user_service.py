import pytest


class TestUserCreation:
    """Тести створення користувачів"""

    @pytest.mark.unit
    def test_create_user_success(self, user_service):
        """Успішне створення користувача"""
        user = user_service.create_user("newuser", "new@test.com", "password123")

        assert user.username == "newuser"
        assert user.email == "new@test.com"
        assert user.is_active is True
        assert user.check_password("password123")

    @pytest.mark.test
    def test_create_duplicate_user(self, user_service):
        """Створення дублікату користувача"""
        user_service.create_user("testuser", "test@test.com", "password123")

        with pytest.raises(ValueError, match="Користувач testuser вже існує"):
            user_service.create_user("testuser", "test2@test.com", "password456")

    @pytest.mark.unit
    def test_create_user_weak_password(self, user_service):
        """Створення користувача зі слабким паролем"""
        with pytest.raises(ValueError, match="Пароль має бути не менше 6 символів"):
            user_service.create_user("testuser", "test@test.com", "123")


class TestAuthentication:
    """Тести аутентифікації"""

    @pytest.mark.unit
    def test_successful_authentication(self, populated_user_service):
        """Успішна аутентифікація"""
        user = populated_user_service.authenticate("admin", "admin123")

        assert user is not None
        assert user.username == "admin"

    @pytest.mark.unit
    def test_wrong_password(self, populated_user_service):
        """Невірний пароль"""
        user = populated_user_service.authenticate("admin", "wrongpassword")
        assert user is None

    @pytest.mark.unit
    def test_nonexistent_user(self, populated_user_service):
        """Неіснуючий користувач"""
        user = populated_user_service.authenticate("nonexistent", "password")
        assert user is None

    @pytest.mark.unit
    def test_deactivated_user(self, populated_user_service):
        """Деактивований користувач"""
        populated_user_service.deactivate_user("user1")
        user = populated_user_service.authenticate("user1", "user123")
        assert user is None


class TestUserRoles:
    """Тести ролей користувачів"""

    @pytest.mark.unit
    def test_add_role(self, sample_user):
        """Додавання ролі"""
        sample_user.add_role("moderator")
        assert sample_user.has_role("moderator")

    @pytest.mark.unit
    def test_duplicate_role(self, sample_user):
        """Додавання дублікату ролі"""
        sample_user.add_role("admin")
        sample_user.add_role("admin")
        assert sample_user.roles.count("admin") == 1

    @pytest.mark.unit
    def test_multiple_roles(self, sample_user):
        """Кілька ролей"""
        sample_user.add_role("admin")
        sample_user.add_role("moderator")

        assert sample_user.has_role("admin")
        assert sample_user.has_role("moderator")
        assert not sample_user.has_role("user")