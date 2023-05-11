import datetime

from django.test import TestCase
from django.urls.base import reverse
from django.utils import timezone

from .models import Question

#Por lo general se testean Modelos o Vistas en entornos profesionales.

class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_questions(self): #creamos la función con el nombre del test
        """returns False for questions whose pub_date is in the future"""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(question_text="¿Quién es el mejor CD de Platzi?", pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_present_questions(self):
        """was_published_recently() must return True for questions whose pub_date is actual"""
        time = timezone.now()
        present_question = Question(question_text="¿Quien es el mejor Course Direct de Platzi?",pub_date=time)
        self.assertIs(present_question.was_published_recently(), True)

def create_question(question_text, days):
    """create a question with the given "question_text" and publishs the given number of days 
    offset to now (negative for questions published in the past, positive for questions that have yet to be published)"""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)    
        
class QuestionIndexViewTests(TestCase):
    
    def test_no_questions(self):
        """If no question exists, an appropiate message is displayed"""
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])
        
    def test_future_question(self):
        """Questions with a pub_date in the fute are display on the index page"""
        create_question("Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"],[])
    
    def test_past_question(self):
        """Questions with a pub_date in the past are displayed on the index page"""
        question = create_question("Past question", days=-10)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [question])
    
    def test_future_question_and_past_question(self):
        """Even if both past and future question exist, only past questions are displayed"""
        past_question = create_question(question_text="Past Question", days=-30)
        future_question = create_question(question_text="Future question", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question])
        
    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        past_question1 = create_question(question_text="Past Question 1", days=-30)
        past_question2 = create_question(question_text="Past question 2", days=-40)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(response.context["latest_question_list"], [past_question1, past_question2])
    

class QuestionDetailViewTest(TestCase):
    
    def test_future_question(self):
        """The detail view of a question with a pub_date in the future returns a 404 error not found"""
        future_question = create_question(question_text="Future question", days=30)
        url = reverse("polls:detail", args=(future_question.pk,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
    
    def test_past_question(self):
        """The detail view of a question with a pub_date in the past displays the question text"""
        past_question = create_question(question_text="Past question", days=30)
        url = reverse("polls:detail", args=(past_question.pk,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
    
    
class ResultsViewTest(TestCase):
    pass

# Create your tests here.
