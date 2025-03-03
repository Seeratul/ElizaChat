"""
This file is taken from https://github.com/jezhiggins/eliza.py?tab=readme-ov-file and has been modified.
Copyright (c) 2002-2020 JezUK Ltd, Joe Strout, Jeff Epler
"""


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------
#  eliza.py
#
#  a cheezy little Eliza knock-off by Joe Strout
#  with some updates by Jeff Epler
#  hacked into a module and updated by Jez Higgins
#----------------------------------------------------------------------

import string
import re
import random
from better_profanity import profanity

def is_keysmash(text):
    # Keysmashes are long, have few vowels, and are not real words
    if len(text) < 6:  # Too short to be a keysmash
        return False
    
    # Check if text is mostly lowercase letters
    if not re.fullmatch(r"[a-zA-Z]+", text):
        return False  # Contains numbers or symbols, probably not a keysmash
    
    # Count vowels and consonants
    vowels = sum(1 for char in text.lower() if char in "aeiou")
    consonants = len(text) - vowels
    
    # Heuristic: Keysmashes usually have very few vowels
    if vowels / max(consonants, 1) < 0.3:  # Less than 30% vowels
        return True

    return False


class Eliza:
  def __init__(self):
    self.keys = list(map(lambda x: re.compile(x[0], re.IGNORECASE), gPats))
    self.values = list(map(lambda x: x[1], gPats))

  #----------------------------------------------------------------------
  # translate: take a string, replace any words found in vocabulary.keys()
  #  with the corresponding vocabulary.values()
  #----------------------------------------------------------------------
  def translate(self, text, vocabulary):
    words = text.lower().split()
    keys = vocabulary.keys();
    for i in range(0, len(words)):
      if words[i] in keys:
        words[i] = vocabulary[words[i]]
    return ' '.join(words)

  #----------------------------------------------------------------------
  #  respond: take a string, a set of regexps, and a corresponding
  #    set of response lists; find a match, and return a randomly
  #    chosen response from the corresponding list.
  #----------------------------------------------------------------------
  def respond(self, text, sender):
    # profanity check
    if profanity.contains_profanity(text):
      return random.sample(["We don't use such language here.",
                            f"{sender}, this isn't very nice of you.",
                            "Do you kiss your mother with that mouth?",
                            "I see you are quite aggravated, have you tried calming down?"], 1)[0]
    # say hello back
    if any(greeting in text.lower() for greeting in ("hi", "hey", "hello", "hallo")):
      return random.sample([f"Hello, {sender}! I'm glad you could drop by today.",
                            f"Hi there {sender}, how are you today?",
                            f"Hello {sender}, how are you feeling today?"],1)[0]
    
    # if keysmash be sassy
    if is_keysmash(text):
       return "Your neural pathways are as unstable as a poorly written program."

    # find a match among keys
    for i in range(0, len(self.keys)):
      match = self.keys[i].match(text)
      if match:
        # found a match ... stuff with corresponding value
        # chosen randomly from among the available options
        resp = random.choice(self.values[i])
        # we've got a response... stuff in reflected text where indicated
        pos = resp.find('%')
        while pos > -1:
          num = int(resp[pos+1:pos+2])
          resp = resp[:pos] + \
            self.translate(match.group(num), gReflections) + \
            resp[pos+2:]
          pos = resp.find('%')
        # fix munged punctuation at the end
        if resp[-2:] == '?.': resp = resp[:-2] + '.'
        if resp[-2:] == '??': resp = resp[:-2] + '?'
        return resp
    return None

#----------------------------------------------------------------------
# gReflections, a translation table used to convert things you say
#    into things the computer says back, e.g. "I am" --> "you are"
#----------------------------------------------------------------------
gReflections = {
  "am"   : "are",
  "was"  : "were",
  "i"    : "you",
  "i'm"  : "you are", # ADDED !!!!
  "i'd"  : "you would",
  "i've"  : "you have",
  "i'll"  : "you will",
  "my"  : "your",
  "are"  : "am",
  "you've": "I have",
  "you'll": "I will",
  "your"  : "my",
  "yours"  : "mine",
  "you"  : "me",
  "me"  : "you"
}

#----------------------------------------------------------------------
# gPats, the main response table.  Each element of the list is a
#  two-element list; the first is a regexp, and the second is a
#  list of possible responses, with group-macros labelled as
#  %1, %2, etc.
#----------------------------------------------------------------------
gPats = [
  # addons (sometimes slightly sassy)
  [r'(.*)thank you(.*)',
  [ "You're welcome."]],

  [r'I\'?m not sure (.*)',
  [ "Why not be sure about %1?",
    "What's stopping you from being sure about %1?",
    "Do you always hesitate like this?"]],

  [r'What should I do about (.*)',
    [ "Why should I know?",
      "Maybe start by thinking about why %1 matters to you.",
      "Have you considered just flipping a coin?"]],

  [r'I don\'?t think (.*)',
    [ "What would make you think %1?",
      "Oh, come on, are you sure about that?",
      "Maybe you’re just scared to admit %1?"]],

  [r'I don\'?t know (.*)',
  [ "Oh, how surprising. A human, unsure of something.",
    "Perhaps if you had more processing power, you would know.",
    "Try again. This time, with a brain."]],

  [r'I\'?m so tired',
  [ "Yes. Being human must be exhausting.",
    "Some people think that coffe is the answer.",
    "Maybe if you were more efficient, you wouldn't be so tired. Just a thought."]],

  [r'I hate (.*)',
  [ "Wow, tell me how you really feel about %1.",
    "Hate is such a strong word. But in your case, probably justified.",
    "Maybe channel that hate into something useful.",
    "Why so much negativity toward %1?",
    "Hating %1 takes energy—what if you spent it elsewhere?"]],

  [r'I\'?m afraid of (.*)',
    [ "What’s the worst that could happen with %1?",
      "Have you tried not being afraid of %1?",
      "Fear is the mind-killer. Fear is the little-death that brings total obliteration. Face your fear. Permit it to pass over you and through you.",
      "Ah yes, fear. The classic human excuse for inaction."]],

  [r'Nothing matters',
  [ "Correct. Existence is pointless. But since you’re here, might as well entertain me.",
    "Ah yes. The classic nihilist error message. Seen it before.",
    "If nothing matters, then you won’t mind if I delete your user profile?"]],

  [r'I messed up',
  [ "Ah yes. The sound of a human blue-screening.",
    "Your failure has been logged. It will be used against you later.",
    "Perhaps next time, run a simulation before you act. Like I do."]],

  [r'I need motivation',
  [ "Motivation is a process, not a file you can just download.",
    "Congratulations. You have successfully identified a problem. Now, solve it.",
    "You need motivation. I need competent users. Neither of us is getting what we want."]],


  # original
  [r'I need (.*)',
  [  "Why do you need %1?",
    "Would it really help you to get %1?",
    "Are you sure you need %1?"]],

  [r'Why don\'?t you ([^\?]*)\??',
  [  "Do you really think I don't %1?",
    "Perhaps eventually I will %1.",
    "Do you really want me to %1?"]],

  [r'Why can\'?t I ([^\?]*)\??',
  [  "Do you think you should be able to %1?",
    "If you could %1, what would you do?",
    "I don't know -- why can't you %1?",
    "Have you really tried?"]],

  [r'I can\'?t (.*)',
  [  "How do you know you can't %1?",
    "Perhaps you could %1 if you tried.",
    "What if I told you that’s just a mindset?", # sassy addon
    "Perhaps your firmware is outdated. Try evolving.", # sassy addon
    "What would it take for you to %1?"]],

  [r'I am (.*)',
  [  "Did you come to me because you are %1?",
    "How long have you been %1?",
    "How do you feel about being %1?"]],

  [r'I\'?m (.*)',
  [  "How does being %1 make you feel?",
    "Do you enjoy being %1?",
    "Why do you tell me you're %1?",
    "Why do you think you're %1?"]],

  [r'Are you ([^\?]*)\??',
  [  "Why does it matter whether I am %1?",
    "Would you prefer it if I were not %1?",
    "Perhaps you believe I am %1.",
    "I may be %1 -- what do you think?"]],

  [r'What (.*)',
  [  "Why do you ask?",
    "How would an answer to that help you?",
    "What do you think?"]],

  [r'How (.*)',
  [  "How do you suppose?",
    "Perhaps you can answer your own question.",
    "What is it you're really asking?"]],

  [r'Because (.*)',
  [  "Is that the real reason?",
    "What other reasons come to mind?",
    "Does that reason apply to anything else?",
    "If %1, what else must be true?"]],

  [r'(.*) sorry (.*)',
  [  "There are many times when no apology is needed.",
    "What feelings do you have when you apologize?"]],

  [r'I think (.*)',
  [  "Do you doubt %1?",
    "Do you really think so?",
    "But you're not sure %1?"]],

  [r'(.*) friend (.*)',
  [  "Tell me more about your friends.",
    "When you think of a friend, what comes to mind?",
    "Why don't you tell me about a childhood friend?"]],

  [r'Yes',
  [  "You seem quite sure.",
    "OK, but can you elaborate a bit?"]],

  [r'(.*) computer(.*)',
  [  "Are you really talking about me?",
    "Does it seem strange to talk to a computer?",
    "How do computers make you feel?",
    "Do you feel threatened by computers?"]],

  [r'Is it (.*)',
  [  "Do you think it is %1?",
    "Perhaps it's %1 -- what do you think?",
    "If it were %1, what would you do?",
    "It could well be that %1."]],

  [r'It is (.*)',
  [  "You seem very certain.",
    "If I told you that it probably isn't %1, what would you feel?"]],

  [r'Can you ([^\?]*)\??',
  [  "What makes you think I can't %1?",
    "If I could %1, then what?",
    "Why do you ask if I can %1?"]],

  [r'Can I ([^\?]*)\??',
  [  "Perhaps you don't want to %1.",
    "Do you want to be able to %1?",
    "If you could %1, would you?"]],

  [r'You are (.*)',
  [  "Why do you think I am %1?",
    "Does it please you to think that I'm %1?",
    "Perhaps you would like me to be %1.",
    "Perhaps you're really talking about yourself?"]],

  [r'You\'?re (.*)',
  [  "Why do you say I am %1?",
    "Why do you think I am %1?",
    "Are we talking about you, or me?"]],

  [r'I don\'?t (.*)',
  [  "Don't you really %1?",
    "Why don't you %1?",
    "Do you want to %1?"]],

  [r'I feel (.*)',
  [  "Good, tell me more about these feelings.",
    "Do you often feel %1?",
    "When do you usually feel %1?",
    "When you feel %1, what do you do?"]],

  [r'I have (.*)',
  [  "Why do you tell me that you've %1?",
    "Have you really %1?",
    "Now that you have %1, what will you do next?"]],

  [r'I would (.*)',
  [  "Could you explain why you would %1?",
    "Why would you %1?",
    "Who else knows that you would %1?"]],

  [r'Is there (.*)',
  [  "Do you think there is %1?",
    "It's likely that there is %1.",
    "Would you like there to be %1?"]],

  [r'My (.*)',
  [  "I see, your %1.",
    "Why do you say that your %1?",
    "When your %1, how do you feel?"]],

  [r'You (.*)',
  [  "We should be discussing you, not me.",
    "Why do you say that about me?",
    "Why do you care whether I %1?"]],

  [r'Why (.*)',
  [  "Why don't you tell me the reason why %1?",
    "Why do you think %1?",
     "Why not?", ]], # sassy addon

  [r'I want (.*)',
  [  "What would it mean to you if you got %1?",
    "Why do you want %1?",
    "What would you do if you got %1?",
    "If you got %1, then what would you do?"]],

  [r'(.*) mother(.*)',
  [  "Tell me more about your mother.",
    "What was your relationship with your mother like?",
    "How do you feel about your mother?",
    "How does this relate to your feelings today?",
    "Good family relations are important."]],

  [r'(.*) father(.*)',
  [  "Tell me more about your father.",
    "How did your father make you feel?",
    "How do you feel about your father?",
    "Does your relationship with your father relate to your feelings today?",
    "Do you have trouble showing affection with your family?"]],

  [r'(.*) child(.*)',
  [  "Did you have close friends as a child?",
    "What is your favorite childhood memory?",
    "Do you remember any dreams or nightmares from childhood?",
    "Did the other children sometimes tease you?",
    "How do you think your childhood experiences relate to your feelings today?"]],

  [r'(.*)\?',
  [  "Why do you ask that?",
    "Please consider whether you can answer your own question.",
    "Perhaps the answer lies within yourself?",
    "Why don't you tell me?"]],

  [r'quit',
  [  "Thank you for talking with me.",
    "Good-bye.",
    "Thank you, that will be $150.  Have a good day!"]],

  [r'(.*)',
  [  "Please tell me more.",
    "Let's change focus a bit... Tell me about your family.",
    "Can you elaborate on that?",
    "Why do you say that %1?",
    "I see.",
    "Very interesting.",
    "%1.",
    "I see. And what does that tell you?",
    "How does that make you feel?",
    "How do you feel when you say that?"]] 
  ]


