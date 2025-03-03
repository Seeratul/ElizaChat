# ElizaChat

Repo for ElizaChat Channel and matching React Client

## The Channel

Our channel is a group therapy with [ELIZA](https://en.wikipedia.org/wiki/ELIZA) as the therapist. 

We used the code provided by Joe Strout, Jeff Epler and Jez Higgins that can be found [here](https://github.com/jezhiggins/eliza.py/blob/main/eliza.py) and added some slight changes to make the conversation a bit more interesting:
- Eliza now responds to profanity which is flagged with the [better_profanity](https://pypi.org/project/better-profanity/) library.
- Eliza now greets users with their name.
- Eliza got a few addons for responses:
    - translating an "i'm" from a user to a "you are" from Eliza which proofed to be essential for conversation flow
    - a custom response to a keysmash
    - a few sassy GLaDOS-style comebacks
    - a Dune reference

Functionality of the Channel:
- old messages get deleted when its cap is reached (25)
- profanity is censored with [better_profanity](https://pypi.org/project/better-profanity/) 

## The React Client 
The client fits the retro theme of Eliza and is modelled after a display of a CRT monitor.

Functionality of the Client: 
- displays channel info in info box
- displays messages in a quickly readable format  
- asks user for name and reuses it for all channels until reload
- does not reload page/scroll back up upon posting a new message
  

 

