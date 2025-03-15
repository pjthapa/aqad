from ..models import Question, Topic
from .genAi import AIGeneratorService


def generateQuestionByTopic(topicId: int) -> Question:
    topic = int(topicId)
    chosen_topic = Topic.objects.get(TOPIC_ID=topic)

    AIservice = AIGeneratorService()
    question = AIservice.create_new_question(topic=chosen_topic)

    new_question = Question(
        QUESTION_NAME=question["question"],
        TOPIC=chosen_topic,
        OPTION_ONE=get_option(question, 1),
        OPTION_TWO=get_option(question, 2),
        OPTION_THREE=get_option(question, 3),
        OPTION_FOUR=get_option(question, 4),
        EXPLANATION_ONE=get_option_explanation(question, 1),
        EXPLANATION_TWO=get_option_explanation(question, 2),
        EXPLANATION_THREE=get_option_explanation(question, 3),
        EXPLANATION_FOUR=get_option_explanation(question, 4),
        CORRECT_ANSWER=question["correct_answer"]
    )

    new_question.save()
    return new_question


def get_option(question, option_choice):
    return question["options"][option_choice - 1][f"{option_choice}"]["option"]


def get_option_explanation(question, option_choice):
    return question["options"][option_choice - 1][f"{option_choice}"]["explanation"]
