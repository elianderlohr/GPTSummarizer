# imports
import openai
from PyPDF2 import PdfReader
import sys


# parameters
openai.api_key = "sk-xxxxxxxxxxxxxxxxxx"

PDF_FILE_PATH = "../example/example.pdf"


# get prompt
def get_prompt(text):
    # read prompt from file
    with open("prompts/summarize.txt", "r") as file:
        prompt = file.read()

    # replace text
    prompt = prompt.replace("{{TEXT_TO_SUMMARIZE}}", text)

    return prompt


# chat gpt 3.5 request
def summarize(text):
    """
    Summarize text using GPT-3.5-Turbo
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a summary generator bot, which creates summaries from texts.",
            },
            {"role": "user", "content": get_prompt(text)},
        ],
        max_tokens=2048,
        temperature=0.7,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    return response["choices"][0]["message"]["content"]


def combine_chunks(summaries):
    """
    Combine chunks of "summaries" array into one string of max 4000 characters
    """
    # combine chunks of "summaries" array into one string of max 4000 characters
    chunks = []

    summary = ""
    for sum in summaries:
        if len(sum) + len(summary) > 4000:
            chunks.append(summary)
            summary = ""

        summary += sum

    if len(chunks) == 0:
        chunks.append(summary)

    return chunks


def main():
    # creating a pdf file object
    reader = PdfReader(PDF_FILE_PATH)

    # page text array
    page_text = []

    # extracting text from page
    for page in reader.pages:
        page_text.append(page.extract_text())

    print("Summarizing text...")

    iterations = 1

    combined_summaries = combine_chunks(page_text)
    print("Found " + str(len(combined_summaries)) + " chunks to summarize.")

    while True:
        if len(combined_summaries) <= 1:
            break

        summaries_of_summaries = []
        # print summaries
        for i, summary in enumerate(combined_summaries):
            print(f"Summarizing summary {i + 1} of {len(combined_summaries)}, iteration {iterations}...")
            summaries_of_summaries.append(summarize(summary))

        print(summaries_of_summaries)
        combined_summaries = combine_chunks(summaries_of_summaries)
        print(combined_summaries)
        iterations += 1

    # summarize last chunk
    print("Summarizing last chunk...")

    final_summary = summarize(combined_summaries[0])

    print("Writing summaries to file...")
    # print summaries_of_summaries to file
    with open("../output/output.txt", "w", encoding="utf-8") as file:
        file.write(final_summary)


if __name__ == "__main__":
    main()
