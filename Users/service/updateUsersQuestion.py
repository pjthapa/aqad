from ..models import User, User_Question, Question, Topic
from django.http import HttpResponse, HttpRequest, JsonResponse
from .generateQuestion import generateQuestionByTopic
from django.forms.models import model_to_dict


def updateUserQuestion(user_id: int) -> HttpResponse:
    try:
        user_object = User.objects.get(USER_ID=user_id)
        topic = user_object.TOPIC
        topic_id = topic.TOPIC_ID

        try:
            latest_user_question = User_Question.objects.filter(TOPIC_id=topic_id).order_by('-QUESTION_ID').first()
            largest_question_id = latest_user_question.QUESTION_ID
        except User_Question.DoesNotExist as e:
            largest_question_id = 0
        except AttributeError as a:
            largest_question_id = 0

        try:
            question_by_topic = Question.objects.filter(QUESTION_ID__gt=largest_question_id.QUESTION_ID).order_by('QUESTION_ID').first()
        except Question.DoesNotExist as e:
            print("No question found for this topic")
            question_by_topic = generateQuestionByTopic(topic.TOPIC_ID)
        except AttributeError as a:
            question_by_topic = generateQuestionByTopic(topic.TOPIC_ID)

        if not question_by_topic:
            print(topic.TOPIC_ID)
            response = generateQuestionByTopic(topic.TOPIC_ID)
            response.save()
            new_user_question = User_Question(
                USER_ID=user_object,
                ANSWERED_ON=True,
                QUESTION_ID=response,
                TOPIC=topic
            )
            new_user_question.save()

            return JsonResponse(model_to_dict(response), safe=False)

        try:
            new_user_question = User_Question(
                USER_ID=user_object,
                ANSWERED_ON=True,
                QUESTION_ID=question_by_topic,
                TOPIC=topic
            )
            new_user_question.save()

        except Exception as e:
            print(type(e))

        print(question_by_topic)

        return JsonResponse(model_to_dict(question_by_topic), safe=False)



    except Exception as e:
        print(type(e))
        return HttpResponse("Unable to find details for the requested user", status=500)