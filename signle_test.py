import asyncio
import datetime

import aiohttp


class SingleTest:
    def __init__(self, fit, resource):
        self.fit = fit
        self.resource = resource
        if not self.resource.endswith("test") and not self.resource.endswith("suite"):
            self.resource += "?suite"

        self.test_command = "%s&format=text" % self.resource
        self.resource = self.resource.split('?')[0]
        self.id = None
        self.status = 'new'

    def set_test(self, test_name):
        pass

    async def run(self):
        print(f"Trying to run test: {self.resource}")
        url = self.fit.get_url(self.test_command)
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    print(r.status_code)
                    print(r.headers)
                    self.id = r.headers['X-FitNesse-Test-Id']
                    text = await r.text()
                    return True
        except asyncio.CancelledError:
            print('Try to stop test gracefully')
            self.stop()
        # send request
        # wait headers
        # set self.id
        # wait until test ends
        # return True if success, False is not success
        # catch cancel and try to stop

    def stop(self):
        print("Trying to stop test: %s, id: %s" % (self.resource, self.id))
        self.fit.send('{%s?responder=stoptest&id=%s' % (self.resource, self.id))

    def fail(self):
        self.status = 'fail'
