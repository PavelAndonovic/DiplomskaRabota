import json
import os
from dotenv import load_dotenv

import openai
from common.prompts import (
    CAUSAL_REASONING_SYSTEM_PROMPT,
    CAUSAL_REASONING_USER_PROMPT
)

from common.result_naming import find_latest_result


def main():
    with open(find_latest_result()) as f:
        result = json.load(f)
    resulting_query = result['query']
    question = result['question']

    answer = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[{"role": "system", "content": CAUSAL_REASONING_SYSTEM_PROMPT},
                  {"role": "user",
                   "content": CAUSAL_REASONING_USER_PROMPT.format(problem=question, query=resulting_query)}],
        temperature=0
    )['choices'][0].message.content

    result['reasoning'] = answer

    with open(find_latest_result(), 'w') as f:
        f.write(json.dumps(result))

    print(answer)


if __name__ == '__main__':
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")
    main()
