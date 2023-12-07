from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth.models import User

from ..views import signup
from ..forms import SignUpForm

class signUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)
    
    def test_signup_url_resolves_signup_view(self):
        view = resolve('/signup/')
        self.assertEqual(view.func, signup)
    
    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')
    
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)
    
    def test_form_inputs(self):
        #The view must contain 5 inputs: csrf, username, email, password1, password2
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)

class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        data = {
            'username':'john',
            'email':'john@gmail.com',
            'password1':'testpass123',
            'password2':'testpass123',
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('home')
    
    def test_redirection(self):
        #A valid form submission should redirect user to homepage
        self.assertRedirects(self.response, self.home_url)
    
    def test_user_creation(self):
        self.assertTrue(User.objects.exists())
    
    def test_user_authentication(self):
        #Create request to arbitrary page.  Page should have a 'user' to its context. after successful signup
        response = self.client.get(self.home_url)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)

class InvalidSignupTests(TestCase):
    def setUp(self):
        url = reverse('signup')
        self.response = self.client.post(url, {}) #Submit empty dictionary
    
    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200) #Invalid submission should return to same page
    
    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)
    
    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())