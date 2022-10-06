def check_palindrome(text):
    if isinstance(text, int) or isinstance(text, float):
        text = str(text)
    if not isinstance(text, str):
        raise TypeError()
    text = text.lower()
    text = text.replace(" ", "")
    text = ''.join([l for l in text if l.isalnum()])
    if text == '':
        return False

    for i in range(len(text) // 2):
        if text[i] != text[-i - 1]:
            return False
        else:
            continue
    return True


test_cases = {
    "abba": True,
    "madAM": True,
    7557: True,
    75.57: True,
    "Wół utył i ma miły tułów.": True,
    "A man, a plan, a canal - Panama": True,
    "Madam, I'm Adam": True,
    "!@#$%^&*())(*&^%$#@!": False,
    "mama": False,
    "      ": False,
    "": False,
    ("abba", "abba"): TypeError(),
    }

for input_value, expectation in test_cases.items():
    if isinstance(expectation, Exception):
        try:
            response = check_palindrome(input_value)
            print(f'Expected {expectation!r} for {input_value!r} got {response!r}')
        except Exception:
            pass
    else:
        response = check_palindrome(input_value)
        assert response == expectation, \
            f'Expected {expectation!r} for {input_value!r} got {response!r}'
    print(input_value, "---PASS")