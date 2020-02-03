def build_messages(complete_message):
    """If a message comes in with more than one json command, need to split
    them and work with each message one by one

    e.g. {"command": "ab", "foo": "bar"}{"command": "cd",
    "bar": "foo"}

    should be returned as

    ['{"command": "ab", "foo": "bar"}',
    '{"command": "cd", "bar": "foo"}']
    """
    separator = "}{"
    if separator not in complete_message:
        # There is only one command
        return [complete_message]
    else:
        # There are multiple commands
        messages = complete_message.split("}{")
        corrected_messages = []
        for message in messages:
            if not message.startswith("{"):
                message = "{" + message
            if not message.endswith("}"):
                message = message + "}"
            corrected_messages.append(message)
        return corrected_messages
