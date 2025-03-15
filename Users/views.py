from django.http import HttpResponse, HttpRequest, JsonResponse
from .models import User, User_Question, Question, Topic
from django.db import IntegrityError
from django.forms.models import model_to_dict
import json
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token

from .service import parseTopicChangeRequest, updateUserQuestion, generateQuestionByTopic

# Create your views here.


class QuestionApi():

    def get_question(self, user_id):

        try:
            return updateUserQuestion(user_id)
        except Exception as e:
            print(type(e))
            return HttpResponse("Unable to find details for the requested user", status=500)

    def check_answer(self, request:HttpRequest):
        pass


@ensure_csrf_cookie
def change_topic(request):
    
    if request.method == "PUT":
        user_id, topic_id = parseTopicChangeRequest(json.loads(request.body))
        user_object = User.objects.get(USER_ID=user_id)
        topic_object = Topic.objects.get(TOPIC_ID=topic_id)
        
        user_object.TOPIC = topic_object
        user_object.save()
        
        return updateUserQuestion(user_id)
    
    else:
        return HttpResponse("Invalid Request Method", status = 405)


def populate_topics(request):
    content_categories = [
    "Biological and Biochemical Foundations of Living Systems: Structure and function of proteins and their constituent amino acids",
    "Biological and Biochemical Foundations of Living Systems: Transmission of genetic information from the gene to the protein",
    "Biological and Biochemical Foundations of Living Systems: Transmission of heritable information from generation to generation and the processes that increase genetic diversity",
    "Biological and Biochemical Foundations of Living Systems: Principles of bioenergetics and fuel molecule metabolism",
    "Biological and Biochemical Foundations of Living Systems: Assemblies of molecules, cells, and groups of cells within single cellular and multicellular organisms",
    "Biological and Biochemical Foundations of Living Systems: The structure, growth, physiology, and genetics of prokaryotes and viruses",
    "Biological and Biochemical Foundations of Living Systems: Processes of cell division, differentiation, and specialization",
    "Biological and Biochemical Foundations of Living Systems: Structure and functions of the nervous and endocrine systems and ways these systems coordinate the organ systems",
    "Biological and Biochemical Foundations of Living Systems: Structure and integrative functions of the main organ systems [this includes the respiratory system, circulatory system, lymphatic system, immune system, digestive system, excretory system, reproductive system, muscles, skeletal system, skin system",
    "Chemical and Physical Foundations of Biological Systems: Translational motion, forces, work, energy, and equilibrium in living systems",
    "Chemical and Physical Foundations of Biological Systems: Importance of fluids for the circulation of blood, gas movement, and gas exchange",
    "Chemical and Physical Foundations of Biological Systems: Electrochemistry and electrical circuits and their elements",
    "Chemical and Physical Foundations of Biological Systems: How light and sound interact with matter",
    "Chemical and Physical Foundations of Biological Systems: Atoms, nuclear decay, electronic structure, and atomic chemical behavior",
    "Chemical and Physical Foundations of Biological Systems: Unique nature of water and its solutions",
    "Chemical and Physical Foundations of Biological Systems: Nature of molecules and intermolecular interactions",
    "Chemical and Physical Foundations of Biological Systems: Separation and purification methods",
    "Chemical and Physical Foundations of Biological Systems: Structure, function, and reactivity of biologically relevant molecules",
    "Chemical and Physical Foundations of Biological Systems: Principles of chemical thermodynamics and kinetics",
    "Biological, psychological, and sociocultural factors influence the ways that individuals perceive, think about, and react to the world: Sensing the environment",
    "Biological, psychological, and sociocultural factors influence the ways that individuals perceive, think about, and react to the world: Making sense of the environment",
    "Biological, psychological, and sociocultural factors influence the ways that individuals perceive, think about, and react to the world: Responding to the world",
    "Biological, psychological, and sociocultural factors influence behavior and behavior change: Individual influences on behavior",
    "Biological, psychological, and sociocultural factors influence behavior and behavior change: Social processes that influence human behavior",
    "Biological, psychological, and sociocultural factors influence behavior and behavior change: Attitude and behavior change",
    "Psychological, sociocultural, and biological factors influence the way we think about ourselves and others, as well as how we interact with others: Self-identity",
    "Psychological, sociocultural, and biological factors influence the way we think about ourselves and others, as well as how we interact with others: Social thinking",
    "Psychological, sociocultural, and biological factors influence the way we think about ourselves and others, as well as how we interact with others: Social interactions",
    "Cultural and social differences influence well-being: Understanding social structure",
    "Cultural and social differences influence well-being: Demographic characteristics and processes",
    "Social stratification and access to resources influence well-being: Social inequality"
    ]
    try:
        for category in content_categories:
            index = category.index(":")
            print(index)
            print(f'TOPIC NAME: {category[:index].strip()}')
            print(f'SUB TOPIC NAME: {category[index:].strip()}')
            new_topic = Topic(
                TOPIC_NAME = category[:index].strip(),
                SUBTOPIC_NAME= category[index:].strip(),
                SUBJECT = "MCAT"
            )
            try:
                new_topic.save()
            except IntegrityError:
                print(f'Unable to save the topic {category}')
                continue
        return HttpResponse("Created new topics")
    except Exception:
        print(Exception)
        return HttpResponse("Failed to create new topics")


@ensure_csrf_cookie
def login(request):
    print(request.POST.get("username"))
    if request.method == "POST":
        raw_data = request.body
        try:
            data = json.loads(raw_data)
            user = User.objects.get(USER_FIRST_NAME=data["username"], USER_LAST_NAME=data["password"])
            return JsonResponse(model_to_dict(user), safe=False)
        except User.DoesNotExist or json.JSONDecodeError:
            return HttpResponse("User not found", status=404)
    else:
        print(request.method)
        return HttpResponse("Invalid Request Method", status=405)

    
def get_csrf(request):
    token = get_token(request)
    print(token)
    return JsonResponse({'csrfToken': token})


def get_all_topics(request):
    """Returns all topics as JSON."""
    topics = Topic.objects.all().values('TOPIC_ID', 'SUBJECT', 'TOPIC_NAME', 'SUBTOPIC_NAME')
    return JsonResponse(list(topics), safe=False)


def generate_question(topic):
    return generateQuestionByTopic(topic)
