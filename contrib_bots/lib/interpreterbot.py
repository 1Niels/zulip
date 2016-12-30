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
            preface messages with "@InterpreterBot".
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
    
    def handle_input(InterpreterBotHandler, original_content, original_sender):
        original_content = original_content.split('```')
        code = original_content[1]
        language = original_content[0].split(' ')[1]
        
        
        
        output = """lang: %s, code:\n```%s```""" % (language, code)
        new_content = output
        return new_content
    
    def handle_message(InterpreterBotHandler, message, client, state_handler):
        original_content = message['content']
        original_sender = message['sender_full_name']
        #code_output = InterpreterBotHandler.handle_input(original_content, original_sender)
        code_output = "Output for [%s' message](http://1niels.zulipdev.org:9991/#narrow/near/%s/stream/%s/topic/%s)" % (message['sender_full_name'],message['id'], message['display_recipient'], message['subject'])
        client.send_message(dict(
            type='stream',
            to=message['display_recipient'],
            subject=message['subject'],
            content= code_output,
        ))

handler_class = InterpreterBotHandler
