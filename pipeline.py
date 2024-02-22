import asyncio
from scrapping import *  # Assuming Scrapper is defined in this module
from utils import call_agents
from prompt import *  # Assuming dataprompt and redprompt are defined here
import logging

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
            prompt=dataprompt, image_url=image_src, model='gpt-4-vision-preview', temperature=0.3)

        logging.info(f"Image description: {image_description}")

        redreturn = call_agents(
            prompt=redprompt, text=f"title:{title}\ncontent:{content}\n{image_description}", model='gpt-4-0125-preview', temperature=0.6)

        logging.info(f"Red return: {redreturn}")
