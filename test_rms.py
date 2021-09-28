import pytest
import time

pytest_plugins = ['errbot.backends.test']
extra_plugin_dir = '.'

trigger_messages = [
    'I use Linux',
    'something something linux someting',
    'LiNuX',
]

@pytest.mark.parametrize('message', trigger_messages)
def test_messages_trigger_bot(testbot, message):
    assert 'GNU' in testbot.exec_command(message)

non_trigger_messages = [
    'I use GNU Linux',
    'Linux and GNU',
    'A message without the l word',
]

@pytest.mark.parametrize('message', non_trigger_messages)
def test_messages_do_not_trigger_bot(testbot, message):
    testbot.push_message(message)
    with pytest.raises(Exception):
        testbot.pop_message(timeout=1)

def test_timeout(testbot):
    testbot.exec_command('!plugin config RMS {"TIMEOUT":3}')

    assert 'GNU' in testbot.exec_command('linux')

    with pytest.raises(Exception):
        testbot.exec_command('linux', timeout=1)

    time.sleep(2)

    assert 'GNU' in testbot.exec_command('linux')
