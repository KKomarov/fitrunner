import asyncio

import aiohttp


class FitErrorBase(Exception):
    pass


class FitnesseTestRunError(FitErrorBase):
    pass


class FitnesseTestStopError(FitErrorBase):
    pass


class FitnesseProcess:
    def __init__(self, **kwargs):
        self.handle = None
        self.port = get_open_port()
        self.process = None
        self.kwargs = kwargs

    async def get_instance(self):
        args = [
            "java", "-jar", r"/binaries/fitnesse-standalone.jar",
            "-p", str(self.port),
        ]

        if self.process is None:
            self.process = await asyncio.create_subprocess_exec(*args)
        print('Pid of created process: %s' % self.process.pid)
        await self.wait()
        return self.process


class Fitnesse:
    def __init__(self, session, host='127.0.0.1'):
        self.session = session
        self.host = host
        self.process = None
        self.all_tests = []

    async def wait(self):
        while True:
            try:
                self.send('')
                return
            except:
                print('Still waiting')
                await asyncio.sleep(1)

    async def run_test(self, test_name):
        test = SingleTest(self, test_name)
        self.all_tests.append(test)
        await test.run()
        return test

    async def stop_all(self):
        await asyncio.gather(*[test.stop() for test in self.all_tests if test.is_stopped()])

    async def send(self, cmd):
        print('Launch command: ', cmd)
        url = self.get_url(cmd)
        print(url)

        async with self.session.get(url) as r:
            print('headers', r.headers)
            print("Run result: ", r.status)
            print(await r.text())

    def get_url(self, resource):
        return f'{self.host}/{resource}'


class SingleTest:
    def __init__(self, fit, resource):
        self.fit = fit
        self.resource = resource.split('?')[0]
        self.is_suite = 'suite' in resource
        # if not self.resource.endswith("test") and not self.resource.endswith("suite"):
        #     self.resource += "?suite"

        self.test_command = self.run_test_url()
        self.id = None
        self.status = 'new'

    def run_test_url(self):
        responder = 'suite' if self.is_suite else 'test'
        return f'{self.resource}?{responder}&format=xml'

    async def run(self):
        print(f"Trying to run test: {self.resource}")
        url = self.fit.get_url(self.test_command)
        try:
            async with self.fit.session.get(url) as r:
                if r.status != 200:
                    raise FitnesseTestRunError(r.status, await r.text())
                print(r.headers)
                self.id = r.headers['X-FitNesse-Test-Id']
                self.status = 'running'
                text = await r.text()
                print('test done', text)
                return True
        except asyncio.CancelledError:
            print('Try to stop test gracefully')
            await asyncio.shield(self.stop())

    def is_stopped(self):
        return self.status == 'stopped'

    async def stop(self):
        if self.status == 'stopped':
            print(f'Test {self.resource} [id={self.id}] already stopped')
            return
        print(f"Trying to stop test {self.resource} [id={self.id}]")
        url = f'{self.resource}?responder=stoptest&id={self.id}'
        url = self.fit.get_url(url)
        try:
            async with self.fit.session.get(url) as r:
                if r.status != 200:
                    raise FitnesseTestStopError(await r.text())
                self.status = 'stopped'
                print('Test stopped', r.status)
        except Exception as e:
            traceback.print_exc()

    def fail(self):
        self.status = 'fail'


import traceback


def get_open_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port
