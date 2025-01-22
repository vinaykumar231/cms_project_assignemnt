from rest_framework.test import APITestCase
from django.urls import reverse
from users.models import User
from content.models import Article
from rest_framework.authtoken.models import Token

class ArticleTests(APITestCase):
    def setUp(self):
        """Set up test data and authentication"""
        # Create test user with all required fields
        self.user = User.objects.create_user(
            email="author@example.com",
            username="author@example.com",
            password="securepass123",
            full_name="Test Author",
            phone="1234567890",
            pincode="123456",
            role="author"
        )
        
        # Create token for authentication
        self.token = Token.objects.create(user=self.user)
        
        # Set up authentication for all requests
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        # Create base test article data
        self.article_data = {
            "title": "Test Article",
            "content": "This is a test article content."
        }
        
        # API endpoints using reverse
        self.list_url = reverse('article-list')

    def test_create_article(self):
        """Test creating a new article"""
        response = self.client.post(self.list_url, self.article_data)
        
        self.assertEqual(response.status_code, 201, 
            f"Failed to create article. Response: {response.data}")
        self.assertEqual(Article.objects.count(), 1)
        self.assertEqual(response.data['title'], self.article_data['title'])
        self.assertEqual(response.data['author_name'], self.user.full_name)

    def test_get_articles(self):
        """Test retrieving articles"""
        # Create a test article
        Article.objects.create(
            title="Sample",
            content="Sample Content",
            author=self.user
        )
        
        response = self.client.get(self.list_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], "Sample")

    def test_update_own_article(self):
        """Test updating own article"""
        article = Article.objects.create(
            title="Original Title",
            content="Original Content",
            author=self.user
        )
        
        update_url = reverse('article-detail', kwargs={'pk': article.pk})
        update_data = {
            "title": "Updated Title",
            "content": "Updated Content"
        }
        
        response = self.client.patch(update_url, update_data)
        
        self.assertEqual(response.status_code, 200,
            f"Failed to update article. Response: {response.data}")
        self.assertEqual(response.data['title'], "Updated Title")

    def test_delete_own_article(self):
        """Test deleting own article"""
        article = Article.objects.create(
            title="To Delete",
            content="Content to delete",
            author=self.user
        )
        
        delete_url = reverse('article-detail', kwargs={'pk': article.pk})
        response = self.client.delete(delete_url)
        
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Article.objects.count(), 0)

    def test_unauthorized_access(self):
        """Test unauthorized access to articles"""
        # Remove authentication
        self.client.credentials()
        
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 401)

    def test_admin_access(self):
        """Test admin access to other user's articles"""
        # Create admin user
        admin_user = User.objects.create_user(
            email="admin@example.com",
            username="admin@example.com",
            password="adminpass123",
            full_name="Test Admin",
            phone="9876543210",
            pincode="654321",
            role="admin"
        )
        
        # Create article by normal user
        article = Article.objects.create(
            title="Author's Article",
            content="Author's Content",
            author=self.user
        )
        
        # Switch to admin user
        admin_token = Token.objects.create(user=admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {admin_token.key}')
        
        # Try to update article
        update_url = reverse('article-detail', kwargs={'pk': article.pk})
        update_data = {
            "title": "Admin Updated",
            "content": "Admin Updated Content"
        }
        
        response = self.client.patch(update_url, update_data)
        self.assertEqual(response.status_code, 200,
            "Admin should be able to update any article")

    def test_other_author_access_denied(self):
        """Test that other authors cannot modify articles"""
        # Create another author
        other_author = User.objects.create_user(
            email="other@example.com",
            username="other@example.com",
            password="otherpass123",
            full_name="Other Author",
            phone="5555555555",
            pincode="555555",
            role="author"
        )
        
        # Create article
        article = Article.objects.create(
            title="Original Article",
            content="Original Content",
            author=self.user
        )
        
        # Switch to other author
        other_token = Token.objects.create(user=other_author)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {other_token.key}')
        
        # Try to update article
        update_url = reverse('article-detail', kwargs={'pk': article.pk})
        update_data = {
            "title": "Unauthorized Update",
            "content": "Unauthorized Content"
        }
        
        response = self.client.patch(update_url, update_data)
        self.assertEqual(response.status_code, 403,
            "Other authors should not be able to modify articles they don't own")