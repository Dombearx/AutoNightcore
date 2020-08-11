from shutil import copyfile
import optparse


class Arg_parser:

    def __init__(self):
        self.parser = optparse.OptionParser()

        self.parser.add_option('-s', '--source',
                               action="store", dest="src",
                               help="source file path")

        self.parser.add_option('-d', '--destination',
                               action="store", dest="dst",
                               help="destination file path")


if __name__ == "__main__":

    parser = Arg_parser().parser

    options, args = parser.parse_args()

    if not options.src or not options.dst:   # if filename is not given
        parser.error('source or destination not given')

    src, dst = options.src, options.dst

    copyfile(src, dst)
