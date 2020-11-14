from mock import patch, Mock
from pytest import raises

from cpu_load_generator.__main__ import input_error_handler


cpu_count = 8


def test_input_error_handler_cpu_count():
    """Test if input_error_handler raises ValueError

    Function input_error_handler raises ValueError when args.cpu_core exceeds
    the number of logical cores in the system.

    """
    mock_args = Mock()

    with patch('cpu_load_generator.__main__.psutil.cpu_count', return_value=cpu_count):
        with raises(ValueError):
            mock_args.cpu_core = 9
            input_error_handler(mock_args)

    mock_args.print_help.assert_called_once()


def test_input_error_handler_duration():
    """Test if input_error_handler raises ValueError.

    Function input_error_handler raises ValueError and prints the help
    when args.duration is below zero.

    """
    mock_args = Mock()

    with patch('cpu_load_generator.__main__.psutil.cpu_count',
               return_value=cpu_count):
        with raises(ValueError):
            mock_args.cpu_core = 0
            mock_args.duration = -1
            input_error_handler(mock_args)

    mock_args.print_help.assert_called_once()


def test_input_error_handler_cpu_load():
    """Test if input_error_handler raises ValueError.

    Function input_error_handler raises ValueError and prints the help
    when args.cpu_load is out of range: (0; 1]

    """
    mock_args = Mock()

    with patch('cpu_load_generator.__main__.psutil.cpu_count',
               return_value=cpu_count):
        with raises(ValueError):
            mock_args.cpu_core = 0
            mock_args.duration = 1
            mock_args.cpu_load = 2
            input_error_handler(mock_args)

    mock_args.print_help.assert_called_once()


def test_input_interface():
    pass


def test_load_all_cores():
    pass


def test_load_single_core():
    pass
