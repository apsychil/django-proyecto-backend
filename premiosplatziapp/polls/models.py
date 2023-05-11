from django.db import models
from django.utils import timezone
import datetime

class Question(models.Model):
    #django establece el id como PK de manera automática.
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    
    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    '''La expresión datetime.timedelta(days=1) es el equivalente a decir "1 dia"
    Es decir que al tiempo ahora le restamos 1 día. Si pub_date es mayor o igual a
    dicha operación, se retorna.
    '''
    
        
class Choice(models.Model):
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text
    
    