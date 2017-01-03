# See readme.md for instructions on running this code.

class InterpreterBotHandler(object):
    '''
    This plugin facilitates explaining programming concepts and
    methods. It looks for messages starting with '@InterpreterBot'
    '''

    def usage(self):
        return '''
            This plugin will allow users to flag messages
            containing code to be evaluated. Users should
            preface messages with "@InterpreterBot". The
            format of the message should be as follows,
            "@InterpreterBot [language] ```[code]```".
            Currently language is limited to python3,
            python, ruby, php, java, go, nodejs, csharp (c#),
            fsharp (f#), cpp (c++), cpp (c++11), and c.
            
            Alternatively users may send "@InterpreterBot
            help" to display help information about the
            bot.
            '''

    def triage_message(self, message, client):
        # return True iff we want to (possibly) response to this message

        original_content = message['content']

        # This next line of code is defensive, as we
        # never want to get into an infinite loop of posting follow
        # ups for own follow ups!
        if message['display_recipient'] == 'InterpreterBot':
            return False
        is_follow_up = (original_content.startswith('@InterpreterBot'))
        return is_follow_up
        
    
    def handle_input(InterpreterBotHandler, original_content, original_sender, message_id, stream, topic):
        supported_languages = ['python3','python', 'ruby', 'php','java','go','nodejs','csharp','fsharp','cpp','cpp11','c']
        try:
            original_content = original_content.split('```')
            code = original_content[1]
        except:
            if original_content[0].lower().find('help') >= 0:
                language = "help"
            else:
                language = "unknown"

        if language in supported_languages:
            output = """lang: %s, code:\n```%s```""" % (language, code)
            bot_message = """[{}](http://1niels.zulipdev.org:9991/#narrow/near/{}/stream/{}/topic/{}) - {}: \n``` {}```
            """.format(original_sender,message_id, stream, topic, language, code)
        elif language.lower() == "help":
            bot_message = 'Interpreter Bot supports the following languages: python'
        else:
            bot_message = original_content
        return bot_message
    
    def handle_message(InterpreterBotHandler, message, client, state_handler):
        original_content = message['content']
        original_sender = message['sender_full_name']
        message_id = message['id']
        stream = message['display_recipient']
        topic = message['subject']
        bot_message = InterpreterBotHandler.handle_input(original_content, original_sender, message_id, stream, topic)
        client.send_message(dict(
            type='stream',
            to=message['display_recipient'],
            subject=message['subject'],
            content= bot_message,
        ))

handler_class = InterpreterBotHandler
