import asyncio
import pytest
from fitnesse import Fitnesse
from signle_test import SingleTest


@pytest.yield_fixture(scope='session')
def fitnesse():
    ft = Fitnesse(1)
    print('Fitnesse setup')
    yield ft
    # stop here
    print('Fitnesse close')
    ft.close()


@pytest.yield_fixture(scope='function')
def teardown(fitnesse):
    single_test = SingleTest(fitnesse, '')
    print('test setup')
    yield single_test
    print(teardown)


# another fixture for teardown

@pytest.mark.parametrize('test_name', [
    'FrontPage.TenSeconds',
    'FrontPage.TenSeconds2',
])
@pytest.mark.asyncio
async def test_a(teardown, test_name):
    teardown.set_test(test_name)
    print('https://asdfas')
    await asyncio.sleep(1)
    assert False


