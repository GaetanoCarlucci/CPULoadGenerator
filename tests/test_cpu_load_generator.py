from mock import patch, Mock
from pytest import raises
from collections import namedtuple

from cpu_load_generator.common._monitor import psutil
from cpu_load_generator.__main__ import input_error_handler, main
from cpu_load_generator._interface import load_all_cores, load_single_core


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


@patch('cpu_load_generator.__main__.argparse')
@patch('cpu_load_generator.__main__.load_single_core')
def test_main_calls_load_single_core(load_single_core_mock, argparse_mock):
    """Test load_single_core is executed as expected.

    :param Mock argparse_mock: argparse module mock

    """
    ParseArgsRetValue = namedtuple('ParseArgsRetValue', 'cpu_core duration cpu_load path_to_profile_json')

    args_mock = Mock()
    argparse_mock.ArgumentParser = Mock(return_value=args_mock)

    args_mock.parse_args = Mock(return_value=ParseArgsRetValue(cpu_core=0, duration=10,
                                                               cpu_load=0.5, path_to_profile_json=""))
    main()

    load_single_core_mock.assert_called_once()


@patch('cpu_load_generator.__main__.argparse')
@patch('cpu_load_generator.__main__.load_all_cores')
def test_main_calls_load_all_cores(load_all_cores_mock, argparse_mock):
    """Test load_all_cores is executed as expected.

    :param Mock argparse_mock: argparse module mock

    """
    ParseArgsRetValue = namedtuple('ParseArgsRetValue', 'cpu_core duration cpu_load path_to_profile_json')

    args_mock = Mock()
    argparse_mock.ArgumentParser = Mock(return_value=args_mock)

    args_mock.parse_args = Mock(return_value=ParseArgsRetValue(cpu_core=-1, duration=10,
                                                               cpu_load=0.5, path_to_profile_json=""))
    main()

    load_all_cores_mock.assert_called_once()


def test_load_single_core():
    with patch('cpu_load_generator.common._monitor.psutil') as psutil_mock:
        psutil_mock.cpu_percent = Mock(return_value=[50])
        load_single_core(0, 1, 0.1)


def test_load_all_cores():
    with patch('cpu_load_generator.common._monitor.psutil') as psutil_mock:
        psutil_mock.cpu_percent = Mock(return_value=[50])
        load_all_cores(1, 0.1)
