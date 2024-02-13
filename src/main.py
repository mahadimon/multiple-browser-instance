
import os, shutil, json
from util import GetProfilePath
from driver import Driver
import asyncio
from configuration import Configuration

settings=""
script_dir = os.path.dirname(os.path.realpath(__file__))

async def ClearProfile(pos):
    profilePath = GetProfilePath(pos)
    if os.path.exists(profilePath):
        shutil.rmtree(profilePath)

async def CreateProfile(posnumbers):
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
    await CreateProfile(configuration.posnumbers)

    for pos in configuration.posnumbers:
        driver: Driver = Driver(GetProfilePath(pos), configuration)
        task = asyncio.create_task(driver.RunBrowser(pos))
        async_tasks.append(task)
    
    asyncio.wait(await asyncio.gather(*async_tasks), timeout=None, return_when=asyncio.ALL_COMPLETED)
    
    await ClearProfile(configuration.posnumbers)

if __name__== "__main__":
    asyncio.run(main())

