import asyncio
import aiohttp
import pytest
from fitnesse import Fitnesse
from signle_test import SingleTest


@pytest.fixture(scope='session')
def event_loop(request):
    """Create an instance of the default event loop for entire run."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
async def fitnesse():
    print(id(asyncio.get_event_loop()))
    async with aiohttp.ClientSession() as session:

        ft = Fitnesse(session, host='http://kkrmaz.rmadproject.org:7080')
        print('Fitnesse setup')
        yield ft
        # stop here

        print('Fitnesse close')


@pytest.mark.parametrize('test_name', [
    'FrontPage.TenSeconds',
    'FrontPage.TenSeconds',
])
@pytest.mark.async_timeout(5)
# @pytest.mark.asyncio
async def test_a(fitnesse, test_name):
    print(id(asyncio.get_event_loop()))
    test = await fitnesse.run_test(test_name)
    print('test result:', test)

# add test pytest.fail() shut downs tests gracefully
