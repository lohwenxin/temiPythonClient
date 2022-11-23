import asyncio
import re
import json

from temi import Temi


def connect(prefix):
    # Test connectivity
    connected = asyncio.get_event_loop().run_until_complete(check_connection(prefix))
    if connected:
        print("Successfully able to query API server")
    else:
        print("Unable to query API server")


async def check_connection(prefix):
    temi = Temi(prefix)
    await temi.connect()
    # await temi.speak(sentence='Hello! I am a robot bot bot').run()
    await goto_position(temi)
    navigation_complete_response = await temi.checkIfNavigationCompleted().run()
    print("Have i completed my previous navigation: ", navigation_complete_response.get('completedNavigation'))

    # await temi.getRemainingDuration().run()
    # await loadMap(temi, "636b1caf9e7e95df37ef99dc")
    # await get_map_list(temi)
    # await goto_position(temi)
    # await goto_location(temi, "pillar")
    # await skid_joy(temi)
    # await get_locations(temi)
    # await call(temi)
    # await get_battery_data(temi)
    # await get_contact(temi)
    return True


async def goto_position(temi):
    await temi.gotoPosition(x=float(2), y=float(2), yaw=float(2.4558), tiltAngle=55).checkIfNavigationCompleted().run()


async def get_locations(temi):
    await temi.getLocations().run()


async def goto_location(temi, location):
    currentPosition = await temi.gotoLocation(location=location).run()
    print(currentPosition)


async def skid_joy(temi, x, y):
    skidJoy_response = await temi.skidJoy(x=float(x), y=float(y)).run()
    split_response = re.split('[= ,]', skidJoy_response.get("position"))
    return [float(split_response[1]), float(split_response[4]), float(split_response[7])]


async def get_map_list(temi):
    mapData = await temi.getMapList().run()
    print("Got map data: ", mapData.get('maps'))


async def loadMap(temi, mapId):
    await temi.loadMap(mapId=mapId).run()


async def call(temi):
    # This is Wen Xin's userID
    await temi.call(userId="c0f9e9c3e12acb97833618235264f870").run()


async def get_battery_data(temi):
    battery_data = await temi.getBatteryData().run()
    print("Got battery data: ", battery_data.get('batteryData'))
    print(float(battery_data.get('batteryData').split('=')[1].split(',')[0]) / 100.0)


async def get_contact(temi):
    contactList = await temi.getContact().run()
    print("Got battery data: ", contactList.get('userinfo'))

if __name__ == '__main__':
    connect("ws://172.16.3.55:8177")
