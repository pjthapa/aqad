from django.db import models
from django.urls import reverse

# Create your models here
# 

class Topic(models.Model):
    """Topic for any subject"""
    TOPIC_ID = models.AutoField(primary_key=True)
    SUBJECT = models.CharField(max_length=100, help_text="Specific subject for the topic")
    TOPIC_NAME = models.CharField(max_length=1000, help_text="Name of the topic")
    SUBTOPIC_NAME = models.CharField(max_length=1000, default="test", help_text="Sub topic name")
    
    def __str__(self) -> str:
        return  self.TOPIC_NAME + self.SUBTOPIC_NAME
    
    class Meta:
        unique_together = ('TOPIC_NAME', 'SUBTOPIC_NAME', 'SUBJECT')
    
    def get_absolute_url(self):
        return reverse('topic-detail', args=[str(self.TOPIC_ID)])

class User(models.Model):
    USER_ID = models.AutoField(primary_key=True)
    USER_FIRST_NAME = models.CharField(max_length=100, help_text="User's first Name")
    USER_LAST_NAME = models.CharField(max_length=100, help_text="USer's last name")
    TOPIC = models.ForeignKey(Topic, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return self.USER_FIRST_NAME + " " + self.USER_LAST_NAME
    
    def get_absolute_url(self):
        """Return the url to access a particular user"""
        return reverse('user-detal', args=[str(self.USER_ID)])
    
    
class Question(models.Model):
    """Question, options, explanation and anwers"""
    QUESTION_ID = models.AutoField(primary_key=True)
    QUESTION_NAME = models.TextField(null=False, help_text="Question Text")
    TOPIC = models.ForeignKey(Topic, on_delete=models.RESTRICT, null=False)
    OPTION_ONE = models.CharField(max_length=1000, null=False, help_text="First Answer Option")
    OPTION_TWO = models.CharField(max_length=1000, null=False, help_text="Second Answer Option")
    OPTION_THREE = models.CharField(max_length=1000, null=False, help_text="First Answer Option")
    OPTION_FOUR = models.CharField(max_length=1000, null=False, help_text="Second Answer Option")
    EXPLANATION_ONE = models.TextField(null=False, help_text="Explanation For the First Answer")
    EXPLANATION_TWO = models.TextField(null=False, help_text="Explanation For the Second Answer")
    EXPLANATION_THREE = models.TextField(null=False, help_text="Explanation For the Third Answer")
    EXPLANATION_FOUR = models.TextField(null=False, help_text="Explanation For the Fourth Answer")
    CORRECT_ANSWER = models.SmallIntegerField(null=False, help_text="Correct Answer Choice")

    def __str__(self) -> str:
        return f"""

        {self.QUESTION_NAME}
        \n
        OPTIONS:
        \n
        {self.OPTION_ONE}\n
        {self.OPTION_TWO}\n
        {self.OPTION_THREE}\n
        {self.OPTION_FOUR}\n

        """


class User_Question(models.Model):
    """Question Details For User"""

    USER_ID = models.ForeignKey(User, on_delete=models.RESTRICT, null=False)
    QUESTION_ID = models.ForeignKey(Question, on_delete=models.RESTRICT, null=False)
    ANSWERED_ON = models.DateTimeField(auto_now_add=True, null=True, help_text="Timestamp For the last Time Question was Sent to the user")
    CORRECTLY_ANSWERED = models.BooleanField(default=False, null=False, help_text="Has User ever answered correctly")
    TOPIC = models.ForeignKey(Topic, on_delete=models.RESTRICT, null=False, help_text="The topic category for this questions")

    class Meta:
        ordering = ['ANSWERED_ON']
        unique_together = ["USER_ID", "QUESTION_ID"]

class Allergen(models.Model):
    """Represents a potential allergen."""
    ALLERGEN_ID = models.AutoField(primary_key=True)
    NAME = models.CharField(max_length=100, unique=True, help_text="Name of the allergen (e.g., Pollen, Peanuts)")

    def __str__(self):
        return self.NAME


class DailyLog(models.Model):
    """Tracks daily health and food information for a user."""
    LOG_ID = models.AutoField(primary_key=True)
    DATE = models.DateField(auto_now_add=True, help_text="The date the log entry was created")

    # Symptom tracking
    HAS_ALLERGIES = models.BooleanField(default=False, help_text="Does the user have allergy symptoms?")
    HAS_COUGH = models.BooleanField(default=False, help_text="Does the user have a cough?")

    # Relational field for specific allergens
    ALLERGENS = models.ManyToManyField(Allergen, blank=True, help_text="Specific allergens the user was exposed to")

    # Flexible field for a list of food items
    FOOD = models.JSONField(default=list, blank=True, help_text="List of food items consumed")

    def __str__(self):
        return f"Log for {self.ALLERGENS} on {self.DATE}"
    