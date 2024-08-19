import openai

# Initialize the OpenAI API key
openai.api_key = "your-api-key-here"

def chat_with_gpt3_5(user_input, conversation):
    """
    Function to chat with GPT-3.5 Turbo.
    :param user_input: The user's input string
    :param conversation: The existing conversation list
    :return: Updated conversation list
    """
    # Append user's message to the conversation
    conversation.append({"role": "user", "content": user_input})

    # API call to GPT-3.5 Turbo
    model_response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation,
        temperature=0,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # Extract and strip the model's message content
    model_output = model_response.choices[0].message['content'].strip()

    # Append model's message to the conversation
    conversation.append({"role": "assistant", "content": model_output})

    return conversation