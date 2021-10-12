#!/usr/bin/env python3
#
# Copyright (c) 2021 LunarG, Inc.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

from base_generator import write
from dx12_base_generator import Dx12BaseGenerator
from dx12_consumer_header_generator import Dx12ConsumerHeaderGenerator, Dx12ConsumerHeaderGeneratorOptions


class Dx12AsciiConsumerHeaderGeneratorOldOptions(
    Dx12ConsumerHeaderGeneratorOptions
):
    """Options for generating a ASCII dump file for Dx12 capture file replay."""

    def __init__(
        self,
        # Path to JSON file listing Vulkan API calls to override on replay.
        constructor_args=None,
        # Path to JSON file listing apicalls and structs to ignore.
        blacklists=None,
        # Path to JSON file listing platform (WIN32, X11, etc.) defined types.
        platform_types=None,
        filename=None,
        directory='.',
        prefix_text='',
        protect_file=False,
        protect_feature=True
    ):
        Dx12ConsumerHeaderGeneratorOptions.__init__(
            self, constructor_args, blacklists, platform_types, filename,
            directory, prefix_text, protect_file, protect_feature
        )


class Dx12AsciiConsumerHeaderGeneratorOld(Dx12ConsumerHeaderGenerator):
    """Generates C++ functions responsible for consuming Dx12 API calls."""

    def generate_feature(self):
        """Methond override."""
        Dx12BaseGenerator.generate_feature(self)
        self.write_struct_functions()
        self.write_dx12_consumer_class('Ascii')

    def write_include(self):
        code = ("\n" "#include \"decode/dx12_ascii_consumer_base.h\"\n" "\n")
        write(code, file=self.outFile)

    def get_consumer_function_body(self, class_name, method_info, return_type):
        return ';'

    def write_struct_functions(self):
        struct_dict = self.source_dict['struct_dict']

        for k, v in struct_dict.items():
            if self.is_struct_black_listed(k):
                continue
            code = 'void WriteStructString(std::ostringstream& oss, const Decoded_{}* value, const char* indent, const bool prefix = false, const bool output = false);\n'.format(
                k
            )
            write(code, file=self.outFile)
