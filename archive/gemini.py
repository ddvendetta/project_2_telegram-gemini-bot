# To run this code you need to install the following dependencies:
# pip install google-genai

# import base64
# import mimetypes
import os
from google import genai
from google.genai import types


# def save_binary_file(file_name, data):
#     f = open(file_name, "wb")
#     f.write(data)
#     f.close()
#     print(f"File saved to to: {file_name}")


def generate():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set. Please set it before running.")
    
    client = genai.Client(api_key=api_key)

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Hello!"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_modalities=[
            "TEXT",
        ],
    )

    file_index = 0
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None
        ):
            continue
        # if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
        #     file_name = f"ENTER_FILE_NAME_{file_index}"
        #     file_index += 1
        #     inline_data = chunk.candidates[0].content.parts[0].inline_data
        #     data_buffer = inline_data.data
        #     file_extension = mimetypes.guess_extension(inline_data.mime_type)
        #     save_binary_file(f"{file_name}{file_extension}", data_buffer)
        # else:
        if chunk.candidates[0].content.parts[0].text:
            print(chunk.candidates[0].content.parts[0].text, end="")

if __name__ == "__main__":
    generate()
