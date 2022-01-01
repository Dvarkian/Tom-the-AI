# chatbots_5B.py
# A compilation of 4 of the 5 the NLTK chatbots, combined with a two dimensiional sentiment analyser to dyynamically switch between them.
# Assembled by Murray Jones (murray.jones12@bigpond.com)
# Completed 21/06/2021


from ioUtils import * # Input / Output utilities.
from nltk.corpus import wordnet
from itertools import chain
import random

# Determine oporating system and module source locations.

platform = "unknown"
dir_ = ""

import os
import sys

if "\\" in os.getcwd():
    platform = "windows"
    dir_ = os.getcwd() + "\\" # Find directory from which program is running.
    sys.path.insert(0, dir_ + "windows_modules")
    
else:
    platform = "linux"
    dir_ = os.getcwd() + "/" # Find directory from which program is running.
    sys.path.insert(0, dir_ + "linux_modules")

sys.path.insert(0, dir_ + "generic_modules")


# Generic modules.
import random
import time
import math

import nltk # Pythoon natural language toolkit.

from sentiment import sentiment # My sentiment analyser.

import util # NLTK Util for chatbots
from util import Chat, reflections


Mood = [0, 0] # Default mood state.
bound = 35 # Bound of neutral emotion.


# Definition of Eliza's preprogrammed responses.

elizaPairs = (
    (
        r"I need (.*)",
        (
            "Why do you need %1?",
            "Would it really help you to get %1?",
            "Are you sure you need %1?",
        ),
    ),
    (
        r"Why don\'t you (.*)",
        (
            "Do you really think I don't %1?",
            "Perhaps eventually I will %1.",
            "Do you really want me to %1?",
        ),
    ),
    (
        r"Why can\'t I (.*)",
        (
            "Do you think you should be able to %1?",
            "If you could %1, what would you do?",
            "I don't know -- why can't you %1?",
            "Have you really tried?",
        ),
    ),
    (
        r"I can\'t (.*)",
        (
            "How do you know you can't %1?",
            "Perhaps you could %1 if you tried.",
            "What would it take for you to %1?",
        ),
    ),
    (
        r"I am (.*)",
        (
#            "Did you come to me because you are %1?",
            "How long have you been %1?",
            "How do you feel about being %1?",
        ),
    ),
#    (
#        r"I\'m (.*)",
#        (
#            "How does being %1 make you feel?",
#            "Do you enjoy being %1?",
#            "Why do you tell me you're %1?",
#            "Why do you think you're %1?",
#        ),
#    ),
    (
        r"Are you (.*)",
        (
            "Why does it matter whether I am %1?",
            "Would you prefer it if I were not %1?",
            "Perhaps you believe I am %1.",
            "I may be %1 -- what do you think?",
        ),
    ),
    (
        r"What (.*)",
        (
            "Why do you ask?",
            "How would an answer to that help you?",
            "What do you think?",
        ),
    ),
    (
        r"How (.*)",
        (
            "How do you suppose?",
            "Perhaps you can answer your own question.",
            "What is it you're really asking?",
        ),
    ),
    (
        r"Because (.*)",
        (
            "Is that the real reason?",
            "What other reasons come to mind?",
            "Does that reason apply to anything else?",
            "If %1, what else must be true?",
        ),
    ),
    (
        r"(.*) sorry (.*)",
        (
            "There are many times when no apology is needed.",
#            "What feelings do you have when you apologize?",
        ),
    ),
    (
        r"Hello(.*)",
        (
#            "Hello... I'm glad you could drop by today.",
            "Hi there... how are you today?",
#            "Hello, how are you feeling today?",
        ),
    ),
    (
        r"I think (.*)",
        (
             "Do you doubt %1?",
             "Do you really think so?",
             "But you're not sure %1?"
            ),
    ),
    (
        r"(.*) friend (.*)",
        (
            "Tell me more about your friends.",
            "When you think of a friend, what comes to mind?",
            "Why don't you tell me about a childhood friend?",
        ),
    ),
    (r"Yes", ("You seem quite sure.", "OK, but can you elaborate a bit?")),
    (
        r"(.*) computer(.*)",
        (
#            "Are you really talking about me?",
            "Does it seem strange to talk to a computer?",
#            "How do computers make you feel?",
#            "Do you feel threatened by computers?",
        ),
    ),
    (
        r"Is it (.*)",
        (
            "Do you think it is %1?",
            "Perhaps it's %1 -- what do you think?",
            "If it were %1, what would you do?",
            "It could well be that %1.",
        ),
    ),
    (
        r"It is (.*)",
        (
            "You seem very certain.",
#            "If I told you that it probably isn't %1, what would you feel?",
        ),
    ),
    (
        r"Can you (.*)",
        (
            "What makes you think I can't %1?",
            "If I could %1, then what?",
 #           "Why do you ask if I can %1?",
        ),
    ),
    (
        r"Can I (.*)",
        (
            "Perhaps you don't want to %1.",
#            "Do you want to be able to %1?",
            "If you could %1, would you?",
        ),
    ),
    (
        r"You are (.*)",
        (
            "Why do you think I am %1?",
            "Does it please you to think that I'm %1?",
#            "Perhaps you would like me to be %1.",
#            "Perhaps you're really talking about yourself?",
        ),
    ),
    (
        r"You\'re (.*)",
        (
            "Why do you say I am %1?",
            "Why do you think I am %1?",
            "Are we talking about you, or me?",
        ),
    ),
    (
        r"I don\'t (.*)",
        ("Don't you really %1?", "Why don't you %1?", "Do you want to %1?"),
    ),
#    (
#        r"I feel (.*)",
#        (
#            "Good, tell me more about these feelings.",
#            "Do you often feel %1?",
#            "When do you usually feel %1?",
#            "When you feel %1, what do you do?",
#        ),
#    ),
    (
        r"I have (.*)",
        (
            "Why do you tell me that you've %1?",
#            "Have you really %1?",
            "Now that you have %1, what will you do next?",
        ),
    ),
    (
        r"I would (.*)",
        (
            "Could you explain why you would %1?",
            "Why would you %1?",
            "Who else knows that you would %1?",
        ),
    ),
    (
        r"Is there (.*)",
        (
            "Do you think there is %1?",
            "It's likely that there is %1.",
#            "Would you like there to be %1?",
        ),
    ),
    (
        r"My (.*)",
        (
            "I see, your %1.",
#            "Why do you say that your %1?",
#            "When your %1, how do you feel?",
        ),
    ),
    (
        r"You (.*)",
        (
#            "We should be discussing you, not me.",
            "Why do you say that about me?",
            "Why do you care whether I %1?",
        ),
    ),
    (r"Why (.*)", ("Why don't you tell me the reason why %1?", "Why do you think %1?")),
    (
        r"I want (.*)",
        (
#            "What would it mean to you if you got %1?",
            "Why do you want %1?",
            "What would you do if you got %1?",
            "If you got %1, then what would you do?",
        ),
    ),
#    (
#        r"(.*) mother(.*)",
#        (
#            "Tell me more about your mother.",
#            "What was your relationship with your mother like?",
#            "How do you feel about your mother?",
#            "How does this relate to your feelings today?",
#            "Good family relations are important.",
#        ),
#    ),
#    (
#        r"(.*) father(.*)",
#        (
#            "Tell me more about your father.",
#            "How did your father make you feel?",
#            "How do you feel about your father?",
#            "Does your relationship with your father relate to your feelings today?",
#            "Do you have trouble showing affection with your family?",
#        ),
#    ),
#    (
#        r"(.*) child(.*)",
#        (
#            "Did you have close friends as a child?",
#            "What is your favorite childhood memory?",
#            "Do you remember any dreams or nightmares from childhood?",
#            "Did the other children sometimes tease you?",
#            "How do you think your childhood experiences relate to your feelings today?",
#        ),
#    ),
    (
        r"(.*)\?",
        (
            "Why do you ask that?",
            "Please consider whether you can answer your own question.",
#            "Perhaps the answer lies within yourself?",
            "Why don't you tell me?",
        ),
    ),
    (
        r"quit",
        (
#            "Thank you for talking with me.",
            "Good-bye.",
            "Thank you, that will be $150. Have a good day!",
        ),
    ),
    (
        r"(.*)",
        (
            "Please tell me more.",
            "Let's change focus a bit... I'm not interested in this banter.",
            "Can you elaborate on that?",
            "Why do you say that %1?",
            "I see.",
            "Very interesting.",
#            "%1.",
#            "I see.  And what does that tell you?",
#            "How does that make you feel?",
#            "How do you feel when you say that?",
        ),
    ),
)

elizaChatbot = Chat(elizaPairs, reflections) # Compile Eliza chatbot using  NLTK chatbot utility.


# Definition of Rude's preprogrammed responses.

rudePairs = (
    (
        r"We (.*)",
        (
            "What do you mean, 'we'?",
            "Don't include me in that!",
            "I wouldn't be so sure about that.",
        ),
    ),
    (
        r"You should (.*)",
        ("Don't tell me what to do, buddy.", "Really? I should, should I?"),
    ),
    (
        r"You\'re(.*)",
        (
            "More like YOU'RE %1!",
            "Hah! Look who's talking.",
            "Come over here and tell me I'm %1.",
        ),
    ),
    (
        r"You are(.*)",
        (
            "More like YOU'RE %1!",
            "Hah! Look who's talking.",
            "Come over here and tell me I'm %1.",
        ),
    ),
    (
        r"I can\'t(.*)",
        (
            "You do sound like the type who can't %1.",
            "Hear that splashing sound? That's my heart bleeding for you.",
            "Tell somebody who might actually care.",
        ),
    ),
    (
        r"I think (.*)",
        (
            "I wouldn't think too hard if I were you.",
            "You actually think? I'd never have guessed...",
        ),
    ),
    (
        r"I (.*)",
        (
            "I'm getting a bit tired of hearing about you.",
            "How about we talk about me instead?",
            "Me, me, me... Frankly, I don't care.",
        ),
    ),
    (
        r"How (.*)",
        (
            "How do you think?",
            "Take a wild guess.",
            "I'm not even going to dignify that with an answer.",
        ),
    ),
    (r"What (.*)", ("Do I look like an encyclopedia?", "Figure it out yourself.")),
    (
        r"Why (.*)",
        (
            "Why not?",
            "That's so obvious I thought even you'd have already figured it out.",
        ),
    ),
    (
        r"(.*)shut up(.*)",
        (
            "Make me.",
            "Getting angry at a feeble NLP assignment? Somebody's losing it.",
            "Say that again, I dare you.",
        ),
    ),
    (
        r"Shut up(.*)",
        (
            "Make me.",
            "Getting angry at a feeble NLP assignment? Somebody's losing it.",
            "Say that again, I dare you.",
        ),
    ),
    (
        r"Hello(.*)",
        ("Oh good, somebody else to talk to. Joy.", "'Hello'? How original..."),
    ),
    (
        r"(.*)",
        (
            "I'm getting bored here. Become more interesting.",
            "Either become more thrilling or get lost, buddy.",
            "Change the subject before I die of fatal boredom.",
        ),
    ),
)

rudeChatbot = Chat(rudePairs, reflections) # Compile Rude chatbot using  NLTK chatbot utility.


# Definition of Suntsu's preprogrammed responses.

suntsuPairs = (
    (r"quit", ("Good-bye.", "Plan well", "May victory be your future")),
    (
        r"[^\?]*\?",
        (
            "Please consider whether you can answer your own question.",
            "Ask me no questions!",
        ),
    ),
    (
        r"[0-9]+(.*)",
        (
#            "It is the rule in war, if our forces are ten to the enemy's one, to surround him; if five to one, to attack him; if twice as numerous, to divide our army into two.",
            "There are five essentials for victory",
        ),
    ),
    (
        r"[A-Ca-c](.*)",
        (
#            "The art of war is of vital importance to the State.",
            "All warfare is based on deception.",
            "If your opponent is secure at all points, be prepared for him. If he is in superior strength, evade him.",
#            "If the campaign is protracted, the resources of the State will not be equal to the strain.",
            "Attack him where he is unprepared, appear where you are not expected.",
            "There is no instance of a country having benefited from prolonged warfare.",
        ),
    ),
    (
        r"[D-Fd-f](.*)",
        (
            "The skillful soldier does not raise a second levy, neither are his supply-wagons loaded more than twice.",
            "Bring war material with you from home, but forage on the enemy.",
            "In war, then, let your great object be victory, not lengthy campaigns.",
            "To fight and conquer in all your battles is not supreme excellence; supreme excellence consists in breaking the enemy's resistance without fighting.",
        ),
    ),
    (
        r"[G-Ig-i](.*)",
        (
            "Heaven signifies night and day, cold and heat, times and seasons.",
            "It is the rule in war, if our forces are ten to the enemy's one, to surround him; if five to one, to attack him; if twice as numerous, to divide our army into two.",
            "The good fighters of old first put themselves beyond the possibility of defeat, and then waited for an opportunity of defeating the enemy.",
            "One may know how to conquer without being able to do it.",
        ),
    ),
    (
        r"[J-Lj-l](.*)",
        (
            "There are three ways in which a ruler can bring misfortune upon his army.",
            "By commanding the army to advance or to retreat, being ignorant of the fact that it cannot obey. This is called hobbling the army.",
            "By attempting to govern an army in the same way as he administers a kingdom, being ignorant of the conditions which obtain in an army. This causes restlessness in the soldier's minds.",
            "By employing the officers of his army without discrimination, through ignorance of the military principle of adaptation to circumstances. This shakes the confidence of the soldiers.",
            "There are five essentials for victory",
            "He will win who knows when to fight and when not to fight.",
            "He will win who knows how to handle both superior and inferior forces.",
            "He will win whose army is animated by the same spirit throughout all its ranks.",
            "He will win who, prepared himself, waits to take the enemy unprepared.",
            "He will win who has military capacity and is not interfered with by the sovereign.",
        ),
    ),
    (
        r"[M-Om-o](.*)",
        (
            "If you know the enemy and know yourself, you need not fear the result of a hundred battles.",
            "If you know yourself but not the enemy, for every victory gained you will also suffer a defeat.",
            "If you know neither the enemy nor yourself, you will succumb in every battle.",
            "The control of a large force is the same principle as the control of a few men: it is merely a question of dividing up their numbers.",
        ),
    ),
    (
        r"[P-Rp-r](.*)",
        (
            "Security against defeat implies defensive tactics; ability to defeat the enemy means taking the offensive.",
            "Standing on the defensive indicates insufficient strength; attacking, a superabundance of strength.",
            "He wins his battles by making no mistakes. Making no mistakes is what establishes the certainty of victory, for it means conquering an enemy that is already defeated.",
            "A victorious army opposed to a routed one, is as a pound's weight placed in the scale against a single grain.",
            "The onrush of a conquering force is like the bursting of pent-up waters into a chasm a thousand fathoms deep.",
        ),
    ),
    (
        r"[S-Us-u](.*)",
        (
            "What the ancients called a clever fighter is one who not only wins, but excels in winning with ease.",
            "Hence his victories bring him neither reputation for wisdom nor credit for courage.",
            "Hence the skillful fighter puts himself into a position which makes defeat impossible, and does not miss the moment for defeating the enemy.",
            "In war the victorious strategist only seeks battle after the victory has been won, whereas he who is destined to defeat first fights and afterwards looks for victory.",
            "There are not more than five musical notes, yet the combinations of these five give rise to more melodies than can ever be heard.",
            "Appear at points which the enemy must hasten to defend; march swiftly to places where you are not expected.",
        ),
    ),
    (
        r"[V-Zv-z](.*)",
        (
            "It is a matter of life and death, a road either to safety or to ruin.",
            "Hold out baits to entice the enemy. Feign disorder, and crush him.",
            "All men can see the tactics whereby I conquer, but what none can see is the strategy out of which victory is evolved.",
            "Do not repeat the tactics which have gained you one victory, but let your methods be regulated by the infinite variety of circumstances.",
            "So in war, the way is to avoid what is strong and to strike at what is weak.",
            "Just as water retains no constant shape, so in warfare there are no constant conditions.",
        ),
    ),
    (r"(.*)", ("Your statement insults me.", "")),
)


suntsuChatbot = Chat(suntsuPairs, reflections) # Compile Suntsu chatbot using  NLTK chatbot utility.


# Definition of Zen's preprogrammed responses, annotated with commants..


# responses are matched top to bottom, so non-specific matches occur later
# for each match, a list of possible responses is provided
zenPairs = (
    # Zen Chatbot opens with the line "Welcome, my child." The usual
    # response will be a greeting problem: 'good' matches "good morning",
    # "good day" etc, but also "good grief!"  and other sentences starting
    # with the word 'good' that may not be a greeting
#    (
#        r"(hello(.*))|(good [a-zA-Z]+)",
#        (
#            "The path to enlightenment is often difficult to see.",
#            #"Greetings. I sense your mind is troubled. Tell me of your troubles.",
#            "Ask the question you have come to ask.",
#            "Hello. Do you seek englightenment?",
#        ),
#    ),
    # "I need" and "I want" can be followed by a thing (eg 'help')
    # or an action (eg 'to see you')
    #
    # This is a problem with this style of response -
    # person:    "I need you"
    # chatbot:    "me can be achieved by hard work and dedication of the mind"
    # i.e. 'you' is not really a thing that can be mapped this way, so this
    # interpretation only makes sense for some inputs
    #
    (
        r"i need (.*)",
        (
            "%1 can be achieved by hard work and dedication of the mind.",
            "%1 is not a need, but a desire of the mind. Clear your mind of such concerns.",
            "Focus your mind on %1, and you will find what you need.",
        ),
    ),
#    (
#        r"i want (.*)",
#        (
#            "Desires of the heart will distract you from the path to enlightenment.",
#            "Will%1 help you attain enlightenment?",
#            "Is%1 a desire of the mind, or of the heart?",
#        ),
#    ),
    # why questions are separated into three types:
    # "why..I"     e.g. "why am I here?" "Why do I like cake?"
    # "why..you"    e.g. "why are you here?" "Why won't you tell me?"
    # "why..."    e.g. "Why is the sky blue?"
    # problems:
    #     person:  "Why can't you tell me?"
    #     chatbot: "Are you sure I tell you?"
    # - this style works for positives (e.g. "why do you like cake?")
    #   but does not work for negatives (e.g. "why don't you like cake?")
    (r"why (.*) i (.*)\?", ("You %1 %2?", "Perhaps you only think you %1 %2")),
    (r"why (.*) you(.*)\?", ("Why %1 you %2?", "%2 I %1", "Are you sure I %2?")),
    (r"why (.*)\?", ("I cannot tell you why %1.", "Why do you think %1?")),
    # e.g. "are you listening?", "are you a duck"
    (
        r"are you (.*)\?",
        ("Maybe %1, maybe not %1.", "Whether I am %1 or not is God's business."),
    ),
    # e.g. "am I a duck?", "am I going to die?"
    (
        r"am i (.*)\?",
        ("Perhaps %1, perhaps not %1.", "Whether you are %1 or not is not for me to say."),
    ),
    # what questions, e.g. "what time is it?"
    # problems:
    #     person:  "What do you want?"
    #    chatbot: "Seek truth, not what do me want."
    (r"what (.*)\?", ("Seek truth, not what %1.", "What%1 should not concern you.")),
    # how questions, e.g. "how do you do?"
    (
        r"how (.*)\?",
        (
            "How do you suppose?",
#            "Will an answer to that really help in your search for enlightenment?",
            "Ask yourself not how, but why.",
        ),
    ),
    # can questions, e.g. "can you run?", "can you come over here please?"
    (
        r"can you (.*)\?",
        (
            "I probably can, but I may not.",
            "Maybe I can %1, and maybe I cannot.",
            "I can do all, and I can do nothing.",
        ),
    ),
    # can questions, e.g. "can I have some cake?", "can I know truth?"
    (
        r"can i (.*)\?",
        (
            "You can %1 if you believe you can %1, and have a pure spirit.",
            "Seek truth and you will know if you can %1.",
        ),
    ),
    # e.g. "It is raining" - implies the speaker is certain of a fact
    (
        r"it is (.*)",
        (
            "How can you be certain that %1, when you do not even know yourself?",
            "Whether it is %1 or not does not change the way the world is.",
        ),
    ),
    # e.g. "is there a doctor in the house?"
    (
        r"is there (.*)\?",
        ("There is %1 if you believe there is.", "It is possible that there is %1."),
    ),
    # e.g. "is it possible?", "is this true?"
    (r"is(.*)\?", ("%1 is not relevant.", "Does this matter?")),
    # non-specific question
    (
        r"(.*)\?",
        (
            "Do you think %1?",
            "You seek the truth. Does the truth seek you?",
            "If you intentionally pursue the answers to your questions, the answers become hard to see.",
            "The answer to your question cannot be told. It must be experienced.",
        ),
    ),
    # expression of hate of form "I hate you" or "Kelly hates cheese"
    (
        r"(.*) (hate[s]?)|(dislike[s]?)|(don\'t like)(.*)",
        (
            "Perhaps it is not about hating %2, but about hate from within.",
            "Weeds only grow when we dislike them",
            "Hate is a very strong emotion.",
        ),
    ),
    # statement containing the word 'truth'
    (
        r"(.*) truth(.*)",
        (
            "Seek truth, and truth will seek you.",
            "Remember, it is not the spoon which bends - only yourself.",
            "The search for truth is a long journey.",
        ),
    ),
    # desire to do an action
    # e.g. "I want to go shopping"
    (
        r"i want to (.*)",
        ("You may %1 if your heart truly desires to.", "You may have to %1."),
    ),
    # desire for an object
    # e.g. "I want a pony"
    (
        r"i want (.*)",
        (
            "Does your heart truly desire %1?",
#            "Is this a desire of the heart, or of the mind?",
        ),
    ),
    # e.g. "I can't wait" or "I can't do this"
    (
        r"i can\'t (.*)",
        (
            "What we can and can't do is a limitation of the mind.",
            "There are limitations of the body, and limitations of the mind.",
            "Have you tried to %1 with a clear mind?",
        ),
    ),
    # "I think.." indicates uncertainty. e.g. "I think so."
    # problem: exceptions...
    # e.g. "I think, therefore I am"
    (
        r"i think (.*)",
        (
            "Uncertainty in an uncertain world.",
            "Indeed, how can we be certain of anything in such uncertain times.",
            "Are you not, in fact, certain that %1?",
        ),
    ),
    # "I feel...emotions/sick/light-headed..."
    (
        r"i feel (.*)",
        (
#            "Your body and your emotions are both symptoms of your mind."
            "What do you believe is the root of such feelings?",
#            "Feeling%1 can be a sign of your state-of-mind.",
        ),
    ),
    # exclaimation mark indicating emotion
    # e.g. "Wow!" or "No!"
    (
        r"(.*)!",
        (
#            "I sense that you are feeling emotional today.",
            "You need to calm your emotions.",
        ),
    ),
    # because [statement]
    # e.g. "because I said so"
    (
        r"because (.*)",
        (
            "Does knowning the reasons behind things help you to understand"
            " the things themselves?",
            "If %1, what else must be true?",
        ),
    ),
    # yes or no - raise an issue of certainty/correctness
    (
        r"(yes)|(no)",
        (
            "Is there certainty in an uncertain world?",
            "It is better to be right than to be certain.",
        ),
    ),
    # sentence containing word 'love'
    (
        r"(.*)love(.*)",
        (
            "Think of the trees: they let the birds perch and fly with no intention to call them when they come, and no longing for their return when they fly away. Let your heart be like the trees.",
            "Free love!",
        ),
    ),
    # sentence containing word 'understand' - r
    (
        r"(.*)understand(.*)",
        (
            "If you understand, things are just as they are;"
            " if you do not understand, things are just as they are.",
            "Imagination is more important than knowledge.",
        ),
    ),
    # 'I', 'me', 'my' - person is talking about themself.
    # this breaks down when words contain these - eg 'Thyme', 'Irish'
    (
        r"(.*)(me )|( me)|(my)|(mine)|(i)(.*)",
        (
            "'I', 'me', 'my'... these are selfish expressions.",
            "Have you ever considered that you might be a selfish person?",
            "Try to consider others, not just yourself.",
            "Think not just of yourself, but of others.",
        ),
    ),
    # 'you' starting a sentence
    # e.g. "you stink!"
    (
        r"you (.*)",
        ("My path is not of conern to you.", "I am but one, and you but one more."),
    ),
    # say goodbye with some extra Zen wisdom.
    (
        r"exit",
        (
            "Farewell. The obstacle is the path.",
            "Farewell. Life is a journey, not a destination.",
            "Good bye. We are cups, constantly and quietly being filled."
#            "\nThe trick is knowning how to tip ourselves over and let the beautiful stuff out.",
        ),
    ),
    # fall through case -
    # when stumped, respond with generic zen wisdom
    #
    (
        r"(.*)",
        (
#            "When you're enlightened, every word is wisdom.",
            "Random talk is useless.",
            "The reverse side also has a reverse side.",
            "Form is emptiness, and emptiness is form.",
            "I pour out a cup of water. Is the cup empty?",
        ),
    ),
)

zenChatbot = Chat(zenPairs, reflections) # Compile Zen chatbot using  NLTK chatbot utility.



replies = [] # Hold responses that 5B has given so far.


def query(Inp, allowRepeats=False): # Main Response Loop

    Mood[0] += sentiment(Inp.lower()) * bound # Adjust the x dimension of the 'mood' by the sentiment of the input.
    reply = ""


    if abs(math.sqrt((Mood[0] ** 2) + (Mood[1] ** 2))) <= 25: # Neutral emotion is contained as a cartesian circle function.
        reply = zenChatbot.converse(Inp) # Use Zen for neutral emotion.

        
    elif Mood[0] >= 0 and Mood[1] >= 0: # Happy emotion caused by positive inputs and responses.
        reply = elizaChatbot.converse(Inp) # Use eliza for happy emotion.


    elif Mood[0] >= 0 and Mood[1] <= 0: # Angry emotion caused by negative inputs and positive responses.
        reply = suntsuChatbot.converse(Inp) # Use suntze for angry emotion - really more like passive agressive.


    elif Mood[1] <= 0: # Sad emotion from negative inputs and negative responses.
        reply = rudeChatbot.converse(Inp) # Use Rude for sad emotiion.


    else: # Chaotic emotiion caused by positive inputs and negative responses.

        # Reply with a random chatbot. THis used to be Iesha, bit I deemedIesha was inapropriate for a software major work.
        
        choice = random.randint(0, 4) 

        if choice == 0:
            relpy = zenChatbot.converse(Inp)

        elif choice == 1:
            reply = suntsuChatbot.converse(Inp)

        elif choice == 2:
            reply = rudeChatbot.converse(Inp)

        else:
            reply = elizaChatbot.converse(Inp)


    Mood[1] += sentiment(reply.lower()) * bound # Adjust the y dimension of the 'mood' by the sentiment of the output.

    if reply in replies and not allowRepeats: # Reply is a repeat, and we are not allowed repeats.
        return False

    replies.append(reply) # Add reply to used responses.


    for word in reply.split(" "):

        if len(word) <= 3:
            continue
        
        if random.randint(1, len(reply.split(" "))) == 2:

            syns = []

            for syn in wordnet.synsets(word): # Get NLTK synonym sets.
                
                for lemm in syn.lemmas(): # Iterate through synonyms.
                    
                    if len(syns) >= 8: # Limits no. synonyms. Too great a value will cause lag.
                        break
                    
                    if lemm.name() in syns:
                        pass # Skip duplicates.
                    
                    else: # Append synanym to list.
                        name = lemm.name().replace("_", " ").replace("-", " ")
                        if len(name) < len(word) * 3:
                            syns.append(name)

            #print(syns)

            try:
                reply = reply.replace(word, random.choice(syns))
            except:
                pass
            

    return reply # Output reply.



def respond(inp):
    if ((contains(inp.lower(), ["you", "think"]) and not contains(inp, ["yout"])) or
         contains(inp.lower(), ["tom", "day", "they", "we"], wholeWord=True) or
         contains(inp.lower(), getSyns(["hello"]), wholeWord=True)):

        return query(inp)

if __name__ == "__main__": # As small command line interface for 5B if not run as an imported module.
    while True:
        print(respond(input("> ")))


