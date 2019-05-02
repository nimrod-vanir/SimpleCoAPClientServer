import logging
import asyncio
import sys
import random
import asyncio
import time

import aiocoap.resource as resource
from aiocoap import *

logging.basicConfig(level=logging.INFO)

async def main():
    """Perform a single PUT request to localhost on the default port, URI
    "/other/block". The request is sent 2 seconds after initialization.

    The payload is bigger than 1kB, and thus sent as several blocks."""

    context = await Context.create_client_context()

    if random.uniform(0, 1) < 0.98:

        start = time.time()

        if(sys.argv[1] == "GET"):
            await asyncio.sleep(random.uniform(0, 2))

            request = Message(code=GET, payload=sys.argv[2].encode('UTF-8'), uri='coap://localhost/.well-known/core')
            try:
                response = await context.request(request).response
            except Exception as e:
                print('Failed to fetch resource:')
                print(e)
            else:
                print('Result: %s\n%r'%(response.code, response.payload))

        elif(sys.argv[1] == "PUT" and sys.argv[2]):
            await asyncio.sleep(random.uniform(0, 2))

            payload = sys.argv[2].encode('UTF-8')
            request = Message(code=PUT, payload=payload, uri="coap://localhost/.well-known/core")

            response = await context.request(request).response

            print('Result: %s\n%r'%(response.code, response.payload))

        #print("RTT: " + str(time.time() - start) + " secs")
        return time.time() - start
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
