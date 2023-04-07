# GPTSummarizer

## How to use?

### 1. Setup

Create a virtual python environment, and install the requirements:
    
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

### 2. Run file
Put your open ai api key in the main.py file under the variable `openai.api_key`. Define the file you want to run and execute the main.py file.
    
    ```bash
    python main.py
    ```

## What does this do?
The tool takes a text file and creates a summary from it. 

It starts by running the text (for each page) from the PDF file through the PyPDF2 library. The script then ensures that no section of text is longer than 4000 characters (a good length for a text that can be passed to the OpenAI API). The script then passes each chunk of text to the OpenAI API with a [prompts](src/prompts/summarize.txt). 

The summaries for each chunk are collected, recombined (respecting the 4000 character limit) and the process repeated.

This is done until only one chunk remains. The final summary is then returned.

## Example
In the example folder is an example pdf file which is summarized using this tool. The example output is also located in the example folder.

Example PDF: [Example PDF](example/example.pdf)

Example Summary: [Example summary](example/example_summary)

