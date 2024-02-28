# Copyright (c) Streamlit Inc. (2018-2022) Snowflake Inc. (2022)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import inspect
import textwrap
from openai import OpenAI
import streamlit as st
import os
import logging


def show_code(demo):
    """Showing the code of the demo."""
    show_code = st.sidebar.checkbox("Show code", True)
    if show_code:
        # Showing the code of the demo.
        st.markdown("## Code")
        sourcelines, _ = inspect.getsourcelines(demo)
        st.code(textwrap.dedent("".join(sourcelines[1:])))


def call_agents(prompt=None, text=None, image_url=None, model=None, temperature=0.7):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    content = []
    if image_url:
        response = call_vision_agent(prompt=prompt, text=text,
                                     image_url=image_url, model=model, temperature=temperature)
        return response.choices[0].message.content
    message = [
        {
            "role": "system",
            "content": prompt
        },
        {
            "role": "user",
            "content": text,
        }
    ]
    logging.info(f"Call agents with message: \n\n\n\n{message}\n\n\n\n")
    logging.info(f"Call agents with model: {model}")
    logging.info(f"Call agents with temperature: {temperature}")
    chat_completion = client.chat.completions.create(
        messages=message,
        model=model,
        temperature=temperature,
        max_tokens=2048
    )
    return chat_completion.choices[0].message.content


def call_vision_agent(prompt=None, text=None, image_url=None, model=None, temperature=0.7):
    client = OpenAI(
        # This is the default and can be omitted
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    response = client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": prompt
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url,
                        },
                    },
                ],
            }
        ],
        max_tokens=2048,
    )
    return response
# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "system",
#             "content": ["You are a helpful assistant."]
#         },
#         {
#             "role": "user",
#             "content": [
#                 {
#                     'text': "Please share the detail information of the chart on different item on a nice structure JSON"
#                 },
#                 {
#                     'image_url': {
#                         "url": "https://www.visualcapitalist.com/wp-content/uploads/2024/02/Share-Of-Global-Forests2.jpg",
#                     },
#                 },
#             ],
#         }
#     ],
#     model="gpt-4-vision-preview",
#     temperature=42
# )
