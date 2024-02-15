
import os, shutil, json
from util import GetProfilePath
from driver import Driver
import asyncio
from configuration import Configuration, PosUser

settings=""
script_dir = os.path.dirname(os.path.realpath(__file__))

async def ClearProfile(posusers: list[PosUser]):
    for posuser in posusers:
        profilePath = GetProfilePath(posuser.posnumber)
        if os.path.exists(profilePath):
            shutil.rmtree(profilePath)

async def CreateProfile(posusers: list[PosUser]):
    for posuser in posusers:
        profilePath = GetProfilePath(posuser.posnumber)
        if os.path.exists(profilePath):
            shutil.rmtree(profilePath)
        os.makedirs(profilePath, exist_ok=True)

async def main():
    async_tasks = []
    with open(os.path.join(script_dir,"configuration.json")) as file:
        settings = json.load(file)
    
    configuration = Configuration(**settings)
    print(configuration.posusers)
    configuration.posusers = [PosUser(**data) for data in configuration.posusers]
    print(configuration.posusers)
    await CreateProfile(configuration.posusers)

    for posuser in configuration.posusers:
        driver: Driver = Driver(GetProfilePath(posuser), configuration)
        task = asyncio.create_task(driver.RunBrowser(posuser))
        async_tasks.append(task)
    
    asyncio.wait(await asyncio.gather(*async_tasks), timeout=None, return_when=asyncio.ALL_COMPLETED)
    
    await ClearProfile(configuration.posusers)

if __name__== "__main__":
    asyncio.run(main())

