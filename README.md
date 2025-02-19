# ElizaChat

https://github.com/jezhiggins/eliza.py?tab=readme-ov-file



# todo
## task 1
- messages only get deleted on refresh/ new msg
- filter content for being off-topic
- deploy

## task 2
The client has to include all functionality of the flask client included in the code but does not need any server code.
- has to list all channels (already done)
- click on channel and have different view where we see channel


                // if then else here
                // if mode is show channel list then 
                <h1>Chat client: List of channels HI AM I THERE</h1>
                <ChannelList />
                // if mode is show channel
                // show channel content
                // <ChannelContent channel_id="1"/>
                
- post messages in channel 
The flask client is very simplistic. Make your React client fancier, somehow.
- 
Add extra functionality to the client, e.g.:
Prompt for the user name only once and the reuse it (either only for this session or also after reloading or restarting the browser)
Build a search function that searches all channels.
Enable formatting like [nop]_word_[/nop| for bold face and [nop]*word*[/nop] for italics
Use the extra field to add some special functions together with your channel (e.g., display buttons to generate an answer)
Add an activity indicator to the channel list, showing the number of unread messages. The indicator should update continuously in the background.
If you are curious and want to invest a bit more, think of a usecase for tensorflow in the browser, (cf. https://www.tensorflow.org/js ) and implement it for your client
The client is deployed on a university server and works with the public hab and the channels registered there.
 