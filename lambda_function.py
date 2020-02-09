import logging
import ask_sdk_core.utils as ask_utils
import json
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from random import randint

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
import boto3
comprehend = boto3.client(service_name='comprehend')

def chooseStr(Ar):
  return Ar[randint(0,len(Ar)-1)]
  
class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Would you like to tell me about how you're feeling?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class EmotionIntentHandler(AbstractRequestHandler):
    """Handler for Hello World Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("EmotionIntent")(handler_input)

        
    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        feelingName = slots["FEELING"].resolutions.resolutions_per_authority[0].values[0].value.name
        feelingValue = slots["FEELING"].name
        
        
             # type: (HandlerInput) -> Response
        speak_output = chooseStr(["Oh you're " + feelingName + ". Why?", "Okay, why do you think you're " + feelingName + "?", "So you're " + feelingName + ". Why's that?"])
        if (feelingName=="feeling sexual desire"):
            speak_output = '<amazon:effect name="whispered">You are feeling horny.</amazon:effect>'
        reprompt = "Would you mind telling me some more?"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt)
                .response
        )
    
class SituationIntentHandler(AbstractRequestHandler):

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> boolnewP
        return ask_utils.is_intent_name("SituationIntent")(handler_input)
    
    def handle(self, handler_input):
        def myToYour(heard):
          stringAr = heard.strip().split(" ")  
          for i in range(len(stringAr)):
            if stringAr[i] == "my":
              stringAr[i] = "your"  
            output = ""  
            for w in stringAr:
                output = output + w + " "  
            output.strip()  
            return output
        def getSentiment(text):
            return(json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True))
        def getKeyWords(text):
            return(json.dumps(comprehend.detect_key_phrases(Text=text, LanguageCode='en'), sort_keys=True))
        slots = handler_input.request_envelope.request.intent.slots
        situation = slots["SITUATION"].value
        sentiment = json.loads(getSentiment(situation))
        keyWords = json.loads(getKeyWords(situation))
        s = sentiment ['Sentiment']
             # type: (HandlerInput) -> Response
        if (s=="NEGATIVE"):
            speak_output = chooseStr(["I'm so sorry to hear that...", "I'm really sorry to hear that...", "That's a big shame...", "Sorry about that..."])
        if (s=="POSITIVE"):
            speak_output = chooseStr(["I'm so glad to hear that...", "That's amazing, I'm happy to hear that... ","I'm happy for you.... ","I'm delighted to hear that... "])
        if (s=='NEUTRAL'):
            speak_output=chooseStr(["Alright, ", "Continue, ", "Okay, ", "Hmmmmm, "]) + chooseStr(["continue.. ", "go on.. ", "that makes sense.. "])
        if (keyWords['KeyPhrases']):
            k = (((keyWords ['KeyPhrases'])[0])['Text'])
        else:
            k = "it"
        speak_output = speak_output + "Let's talk more about " +(myToYour(k))
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask("Are you still there?")
                .response
        )    
class PolarIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("PolarIntent")(handler_input)

    def handle(self, handler_input):
        slots = handler_input.request_envelope.request.intent.slots
        aff = len(str(slots["AFFIRMATION"]))
        neg = len(str(slots["NEGATION"]))
        if (neg>250):
            speak_output = "Okay, I'm sorry"
        if (aff>250):
            speak_output =chooseStr(["Okay, ","Alright, ","Sure, "])+ chooseStr(["would you like to ","do you want to ", "how about you ", "why don't you "] + chooseStr["tell me some more?","talk more about it?","keep talking about it"])
        # type: (HandlerInput) -> Response

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class OpinionIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("OpinionIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output =  chooseStr(["What do you think?","I don't know bro, what do you think?","Not sure, Any thoughts of your own?", "Would you mind telling my some more?","Keep going?"])

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):

        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "I'm sorry, I don't really know what you mean..."
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(EmotionIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(OpinionIntentHandler())
sb.add_request_handler(PolarIntentHandler())
sb.add_request_handler(SituationIntentHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
