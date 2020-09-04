import boto3
import os

def lex_aws_connection():
    client = boto3.client('lex-runtime', region_name=os.getenv("REGION_NAME", 
        "us-east-1"))

    return client


def translate_aws_connection():
    client = boto3.client('translate', region_name=os.getenv("REGION_NAME", 
        "us-east-1"))

    return client


def translate_text(client, text, source_code, target_code):

    response = client.translate_text(
        Text = text,
        SourceLanguageCode = source_code,
        TargetLanguageCode = target_code
    )

    print(f"INFO: Traduzindo {text} de {source_code} para {target_code}")

    translated = response.get("TranslatedText")
    return translated


# TODO: Create a separeted lambda session to create Lex Session with Cognito
def create_session(client, user_id):
    bot_name = os.getenv("BOT_NAME", "FitecDemo")
    bot_alias = os.getenv("BOT_ALIAS", "dev")

    response = client.put_session(
        botName = bot_name,
        botAlias = bot_alias,
        userId = user_id
    )

    return response


def post_text_to_bot(client, user_id, text):
    bot_name = os.getenv("BOT_NAME", "FitecDemo")
    bot_alias = os.getenv("BOT_ALIAS", "dev")

    response = client.post_text(
        botName = bot_name,
        botAlias = bot_alias,
        userId = user_id,
        inputText=text
    )
    print(f"INFO: Message log {user_id}")
    message = response.get("message")

    return message
    