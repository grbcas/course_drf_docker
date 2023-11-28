from habits.services.telegram import telegram_bot_message


def test_telegram_bot_message():
    response = telegram_bot_message("test", '559773959')
    response = {'ok': True,
                'result': {'message_id': 140, 'from': {'id': 6542037151, 'is_bot': True, 'first_name': 'skybot_27',
                                                       'username': 'skybot27_bot'},
                           'chat': {'id': 559773959, 'first_name': 'Alexander', 'username': 'grbcas',
                                    'type': 'private'}, 'date': 1701194543,
                           'text': 'test'}}

    assert response['ok'] is True
