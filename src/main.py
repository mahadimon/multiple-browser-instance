
import os, shutil, json
from util import GetProfilePath
from driver import Driver
import asyncio
from configuration import Configuration

settings=""
script_dir = os.path.dirname(os.path.realpath(__file__))

def ClearProfile(posnumbers):
    for pos in posnumbers:
        profilePath = GetProfilePath(pos)
        if os.path.exists(profilePath):
            shutil.rmtree(profilePath)

def CreateProfile(posnumbers):
    for pos in posnumbers:
        profilePath = GetProfilePath(pos)
        if os.path.exists(profilePath):
            shutil.rmtree(profilePath)
        os.makedirs(profilePath, exist_ok=True)

async def main():
    async_tasks = []
    with open(os.path.join(script_dir,"configuration.json")) as file:
        settings = json.load(file)
    
    configuration = Configuration(**settings)
    CreateProfile(configuration.posnumbers)

    for pos in configuration.posnumbers:
        driver: Driver = Driver(GetProfilePath(pos), configuration)
        async_tasks.append(asyncio.create_task(driver.RunBrowser(pos)))
    
    await asyncio.gather(*async_tasks).add_done_callback(ClearProfile)

if __name__== "__main__":
    asyncio.run(main())

