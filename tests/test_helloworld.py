# Test that uade_battleship.main.main() prints 'Hello, world!' to stdout.
#
from uade_battleship.main import main


def test_main(capsys):
    main()
    out, err = capsys.readouterr()
    assert out == "Hello, world!\n"
    assert err == ""
