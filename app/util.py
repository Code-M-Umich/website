# For data that would clog up other files
import random
import config
from flask import request

def get_current_user():
    if config.USER is '':
        return request.environ['REMOTE_USER'] #should always be valid with cosign
    return 'devUser'


compliments = [
"You look wonderful today", 
"You're cool",
"Your smile is contagious",
"You look great today",
"You're a smart cookie",
"I like your style",
"You have the best laugh",
"I appreciate you",
"Your perspective is refreshing",
"You're an awesome friend",
"You light up the room",
"You deserve a hug right now",
"You should be proud of yourself",
"You have a great sense of humor",
"You've got all the right moves",
"On a scale from 1 to 10, you're an 11",
"You are brave",
"Your eyes are breathtaking",
"You are making a difference",
"You're like sunshine on a rainy day",
"You bring out the best in other people",
"You're a great listener",
"I bet you sweat glitter",
"That color is perfect on you",
"Hanging out with you is always a blast",
"Being around you makes everything better",
"You're wonderful",
"Jokes are funnier when you tell them",
"Your hair looks stunning",
"You're one of a kind",
"You're inspiring",
"Our community is better because you're in it",
"You have the best ideas",
"You're a great example to others",
"You could survive a Zombie apocalypse",
"You're more fun than bubble wrap",
"Any team would be lucky to have you on it",
"I bet you do the crossword puzzle in ink",
"You're someone's reason to smile",
"You have a good head on your shoulders.",
"You're really something special",
"You're a gift to those around you"
]


def randomCompliment():
    return random.choice(compliments)

