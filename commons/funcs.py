import re
from configs import bot
from commons.exceptions import AskCanceled, WrongAnswerReached
from commons.texts import (OPERATION_CANCELED_TEXT, REACH_MAX_WRONG_ANSWERS_TEXT,
                           TIMEOUT_ERROR_TEXT, ANSWER_REACH_MAX_LENGTH_TEXT, CANCEL_OPERATION_TEXT)


async def hinted_ask(chat_id, ask_text, hint_text, correct_answer_regex,
                     accept_wrongs_count=3, cancel_option=True, answer_max_lentgh=None,
                     force_type=None, *args, **kwargs):
    have_wrong = False

    if cancel_option:
        ask_text += '\n\n' + CANCEL_OPERATION_TEXT
        hint_text += '\n\n' + CANCEL_OPERATION_TEXT

    while accept_wrongs_count != 0:
        try:
            asked = await bot.ask(chat_id=chat_id, text=hint_text if have_wrong else ask_text, *args, **kwargs)
            answer = asked.text if asked.text else asked.caption
            answer = answer if answer else ''
            try:
                if answer_max_lentgh and answer_max_lentgh <= len(answer):
                    await bot.send_message(chat_id=chat_id, text=ANSWER_REACH_MAX_LENGTH_TEXT.format(
                        answer_max_lentgh=answer_max_lentgh
                    ))
                    accept_wrongs_count -= 1
                    continue
            except TypeError:
                pass
        except TimeoutError:
            accept_wrongs_count -= 1
            continue

        if answer == '/cancel':
            raise AskCanceled

        if force_type:
            if getattr(asked, force_type):
                return asked
        elif type(correct_answer_regex) == list:
            for regex in correct_answer_regex:
                if re.match(regex, answer):
                    return asked
        elif re.match(correct_answer_regex, answer):
            return asked

        accept_wrongs_count -= 1
        have_wrong = True
    else:
        raise WrongAnswerReached


async def hinted_ask_str(*args, **kwargs) -> str:
    try:
        obj = await hinted_ask(*args, **kwargs)
        return obj.text
    except TimeoutError:
        text = TIMEOUT_ERROR_TEXT
    except WrongAnswerReached:
        text = REACH_MAX_WRONG_ANSWERS_TEXT
    except AskCanceled:
        text = OPERATION_CANCELED_TEXT
    chat_id = kwargs.get('chat_id')
    await bot.send_message(chat_id=chat_id, text=text)
