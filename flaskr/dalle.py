import openai
import sys


# Initialize the OpenAI API key
openai.api_key = "Place your API key here.."

def dalleapp(user_input):

    # API call to GPT-3.5 Turbo
    model_response = openai.Image.create(
  prompt=user_input,
  n=1,
  size="1024x1024"
)

    model_output = model_response['data'][0]['url']
    return model_output

if __name__ == "__main__":
    user_input = sys.argv[1]  # Accept user input from command line argument
    output = dalleapp(user_input)
    print(output)


   