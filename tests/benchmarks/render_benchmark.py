# Copyright 2016 The Spitfire Authors. All Rights Reserved.
#
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import copy
import optparse
import timeit

try:
    import spitfire
    import spitfire.compiler.util
    import spitfire.compiler.options
except ImportError:
    spitfire = None

TABLE_DATA = [
    dict(a=1,
         b=2,
         c=3,
         d=4,
         e=5,
         f=6,
         g=7,
         h=8,
         i=9,
         j=10) for x in range(1000)
]


def get_spitfire_tests():
    if not spitfire:
        return []

    tmpl_src = """
        <table>
            #for $row in $table
                <tr>
                    #for $column in $row.values()
                        <td>$column</td>
                    #end for
                </tr>
            #end for
        </table>
    """

    tmpl_search_list = [{'table': TABLE_DATA}]

    default_opts = spitfire.compiler.options.default_options
    o1_opts = spitfire.compiler.options.o1_options
    o2_opts = spitfire.compiler.options.o2_options
    o3_opts = spitfire.compiler.options.o3_options

    def _spitfire_baked_opts(o):
        o = copy.copy(o)
        o.baked_mode = True
        o.generate_unicode = False
        return o

    baked_opts = _spitfire_baked_opts(default_opts)
    baked_o1_opts = _spitfire_baked_opts(o1_opts)
    baked_o2_opts = _spitfire_baked_opts(o2_opts)
    baked_o3_opts = _spitfire_baked_opts(o3_opts)

    tmpl = spitfire.compiler.util.load_template(tmpl_src,
                                                'tmpl',
                                                analyzer_options=default_opts)

    tmpl_o1 = spitfire.compiler.util.load_template(tmpl_src,
                                                   'tmpl_o1',
                                                   analyzer_options=o1_opts)

    tmpl_o2 = spitfire.compiler.util.load_template(tmpl_src,
                                                   'tmpl_o2',
                                                   analyzer_options=o2_opts)

    tmpl_o3 = spitfire.compiler.util.load_template(tmpl_src,
                                                   'tmpl_o3',
                                                   analyzer_options=o3_opts)

    tmpl_baked = spitfire.compiler.util.load_template(
        tmpl_src,
        'tmpl_baked',
        analyzer_options=baked_opts)

    tmpl_baked_o1 = spitfire.compiler.util.load_template(
        tmpl_src,
        'tmpl_baked_o1',
        analyzer_options=baked_o1_opts)

    tmpl_baked_o2 = spitfire.compiler.util.load_template(
        tmpl_src,
        'tmpl_baked_o2',
        analyzer_options=baked_o2_opts)

    tmpl_baked_o3 = spitfire.compiler.util.load_template(
        tmpl_src,
        'tmpl_baked_o3',
        analyzer_options=baked_o3_opts)

    tmpl_unfiltered = spitfire.compiler.util.load_template(
        tmpl_src,
        'tmpl_unfiltered',
        analyzer_options=default_opts,
        compiler_options={'enable_filters': False})

    tmpl_unfiltered_o1 = spitfire.compiler.util.load_template(
        tmpl_src,
        'tmpl_unfiltered_o1',
        analyzer_options=o1_opts,
        compiler_options={'enable_filters': False})

    tmpl_unfiltered_o2 = spitfire.compiler.util.load_template(
        tmpl_src,
        'tmpl_unfiltered_o2',
        analyzer_options=o2_opts,
        compiler_options={'enable_filters': False})

    tmpl_unfiltered_o3 = spitfire.compiler.util.load_template(
        tmpl_src,
        'tmpl_unfiltered_o3',
        analyzer_options=o3_opts,
        compiler_options={'enable_filters': False})

    def test_spitfire():
        """Spitfire template"""
        tmpl(search_list=tmpl_search_list).main()

    def test_spitfire_o1():
        """Spitfire template -O1"""
        tmpl_o1(search_list=tmpl_search_list).main()

    def test_spitfire_o2():
        """Spitfire template -O2"""
        tmpl_o2(search_list=tmpl_search_list).main()

    def test_spitfire_o3():
        """Spitfire template -O3"""
        tmpl_o3(search_list=tmpl_search_list).main()

    def test_spitfire_baked():
        """Spitfire template baked"""
        tmpl_baked(search_list=tmpl_search_list).main()

    def test_spitfire_baked_o1():
        """Spitfire template baked -O1"""
        tmpl_baked_o2(search_list=tmpl_search_list).main()

    def test_spitfire_baked_o2():
        """Spitfire template baked -O2"""
        tmpl_baked_o2(search_list=tmpl_search_list).main()

    def test_spitfire_baked_o3():
        """Spitfire template baked -O3"""
        tmpl_baked_o3(search_list=tmpl_search_list).main()

    def test_spitfire_unfiltered():
        """Spitfire template unfiltered"""
        tmpl_unfiltered(search_list=tmpl_search_list).main()

    def test_spitfire_unfiltered_o1():
        """Spitfire template unfiltered -O1"""
        tmpl_unfiltered_o2(search_list=tmpl_search_list).main()

    def test_spitfire_unfiltered_o2():
        """Spitfire template unfiltered -O2"""
        tmpl_unfiltered_o2(search_list=tmpl_search_list).main()

    def test_spitfire_unfiltered_o3():
        """Spitfire template unfiltered -O3"""
        tmpl_unfiltered_o3(search_list=tmpl_search_list).main()

    return [
        test_spitfire,
        test_spitfire_o1,
        test_spitfire_o2,
        test_spitfire_o3,
        test_spitfire_baked,
        test_spitfire_baked_o1,
        test_spitfire_baked_o2,
        test_spitfire_baked_o3,
        test_spitfire_unfiltered,
        test_spitfire_unfiltered_o1,
        test_spitfire_unfiltered_o2,
        test_spitfire_unfiltered_o3,
    ]


spitfire_tests = get_spitfire_tests()


def time_test(test, number):
    # Put the test in the global scope for timeit.
    name = 'timeit_%s' % test.__name__
    globals()[name] = test
    # Time the test.
    timer = timeit.Timer(setup='from __main__ import %s;' % name,
                         stmt='%s()' % name)
    time = timer.timeit(number=number) / number
    if time < 0.00001:
        result = '   (not installed?)'
    else:
        result = '%16.2f ms' % (1000 * time)
    print '%-35s %s' % (test.__doc__, result)


def run_tests(which=None, number=100):
    if number > 100:
        print 'Running benchmarks %d times each...' % number
        print
    groups = ['spitfire',]
    # Built the full list of eligible tests.
    tests = []
    for g in groups:
        test_list = '%s_tests' % g
        tests.extend(globals()[test_list])
    # Optionally filter by a set of matching test name (sub)strings.
    if which:
        which_tests = []
        for t in tests:
            for w in which:
                if w.lower() in t.__name__.lower():
                    which_tests.append(t)
        tests = which_tests
    # Run the tests.
    for t in tests:
        time_test(t, number)


def profile_tests(which=None):
    print 'Profiling...'
    print
    import hotshot, hotshot.stats
    profile_data = 'template.prof'
    profile = hotshot.Profile(profile_data)
    profile.runcall(run_tests, which=which, number=1)
    stats = hotshot.stats.load(profile_data)
    stats.strip_dirs()
    stats.sort_stats('time', 'calls')
    print
    stats.print_stats()
    print 'Profile data written to %s' % profile_data


def main():
    option_parser = optparse.OptionParser()
    option_parser.add_option('-p',
                             '--profile',
                             action='store_true',
                             default=False)
    option_parser.add_option('-n', '--number', type='int', default=100)
    (options, args) = option_parser.parse_args()

    if options.profile:
        profile_tests(which=args)
    else:
        run_tests(which=args, number=options.number)


if __name__ == '__main__':
    main()