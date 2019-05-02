import datetime
import logging

import asyncio

import aiocoap.resource as resource
import aiocoap


class IoTResource(resource.Resource):
    """Example resource which supports the GET and PUT methods. It sends large
    responses, which trigger blockwise transfer."""

    def __init__(self):
        super().__init__()
        self.resourceDict = {}
        self.resourceDict["temp"] = "32.5"
        self.resourceDict["humidity"] = "10"
        self.resourceDict["pressure"] = "101.325"
        self.resourceDict["light"] = "85.5"
        self.resourceDict["altitiude"] = "1000"

    def set_content(self, content):
        key = content.decode('UTF-8').split(":")[0]
        value = content.decode('UTF-8').split(":")[1]
        self.resourceDict[key] = value
        self.content = content


    async def render_get(self, request):
        requestPayload = request.payload.decode('UTF-8')
        if requestPayload == "all":
            return aiocoap.Message(payload=str(self.resourceDict).encode('UTF-8'))
        elif requestPayload in self.resourceDict:
            return aiocoap.Message(payload=str(self.resourceDict[requestPayload]).encode('UTF-8'))
        else:
            return aiocoap.Message(payload="INVALID REQUEST".encode('UTF-8'))

    async def render_put(self, request):
        print('PUT payload: %s' % request.payload)
        self.set_content(request.payload)
        return aiocoap.Message(code=aiocoap.CHANGED, payload=self.content)

# logging setup

logging.basicConfig(level=logging.INFO)
logging.getLogger("coap-server").setLevel(logging.DEBUG)

def main():
    # Resource tree creation
    root = resource.Site()

    #root.add_resource(('.well-known', 'core'),
            #resource.WKCResource(root.get_resources_as_linkheader))
    root.add_resource(('.well-known', 'core'), IoTResource())

    asyncio.Task(aiocoap.Context.create_server_context(root))

    asyncio.get_event_loop().run_forever()

if __name__ == "__main__":
    main()
