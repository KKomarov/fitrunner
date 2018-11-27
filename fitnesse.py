import asyncio
import aiohttp


class Fitnesse:
    def __init__(self, max_runners):
        self.host = '127.0.0.1'
        self.port = get_open_port()
        self.process = None
        self.sem = asyncio.Semaphore(max_runners)

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

    async def wait(self):
        while True:
            try:
                self.send('')
                return
            except:
                print('Still waiting')
                await asyncio.sleep(1)

    def get_url(self, resource):
        host, port = self.host, self.port
        url = 'http://{host}:{port}/{resource}'.format(**locals())
        return url

    def send(self, cmd):
        import requests
        print('Launch command: ', cmd)
        url = self.get_url(cmd)
        print(url)
        r = requests.get(url)
        print("Run result: ", r.status_code)
        print(r.text)
    def close(self):
        pass


def get_open_port():
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port
