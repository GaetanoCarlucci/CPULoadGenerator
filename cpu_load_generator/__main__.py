import argparse

import psutil

from cpu_load_generator import load_all_cores, load_single_core


def parse_args(parser):
    """Parse input parameters.

    param parser: ArgumentParser object

    """

    parser.add_argument('-l', '--cpu_load', type=float, help='Cpu target load.', required=True)
    parser.add_argument('-d', '--duration', type=int, required=True,
                        help='Duration of the load in seconds. Should be higher than 0.')
    parser.add_argument('-c', '--cpu_core', type=int, default=0,
                        help='Select the CPU number on which generate the load. Default is 0.')
    args = parser.parse_args()

    return args


def input_error_handler(args):
    """Handle input errors.

    param args: parsed input arguments
    type args: object

    """
    cpu_count = psutil.cpu_count()
    if not args.cpu_core < cpu_count:
        args.print_help()
        raise ValueError('Core to load should not be higher than {}!'.format(cpu_count - 1))
    if args.duration < 0:
        args.print_help()
        raise ValueError('The load duration must be higher then 0!')
    if not 0 < args.cpu_load <= 1.0:
        args.print_help()
        raise ValueError('CPU load time should be the fraction of 1. Range (0; 1].')


def main():
    """The main package entry point."""
    parser = argparse.ArgumentParser()
    args = parse_args(parser)

    input_error_handler(args)

    if args.cpu_core >= 0:
        load_single_core(args.cpu_core, args.duration, args.cpu_load)
    else:
        load_all_cores(args.duration, args.cpu_load)


if __name__ == "__main__":
    main()
