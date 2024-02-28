import asyncio
from scrapping import *  # Assuming Scrapper is defined in this module
from utils import *
from prompt import *  # Assuming dataprompt and redprompt are defined here
import logging
import json
# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


async def scrapping():
    scrapper = Scrapper()
    return await scrapper.scrap_from_website(visualCapitalist)


if __name__ == "__main__":
    title, content, image_src = asyncio.run(scrapping())
    if image_src:
        image_description = call_agents(
            prompt=dataprompt,
            text="请根据图片描述。",
            image_url=image_src,
            model='gpt-4-vision-preview',
            temperature=0.3)

        logging.info(f"Image description: {image_description}")

        redreturn = call_agents(
            prompt=redprompt,
            text=f"""
                标题:{title}
                内容:{content}
                    {image_description}""",
            model='gpt-4-0125-preview',
            temperature=0.3)

        logging.info(f"Red return: {redreturn}")

    if redreturn:
        title, content = json_parsing(redreturn)
