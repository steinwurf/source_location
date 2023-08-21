#!  /usr/bin/env python
# encoding: utf-8


APPNAME = "fmt"
VERSION = "3.0.0"


def configure(conf):
    conf.set_cxx_std(11)


def build(bld):
    # Path to the source_location repo
    source_location_path = bld.dependency_node("source_location-source")

    # Create system include for source_location
    source_location_include = source_location_path.find_dir("include")

    bld(
        name="source_location",
        export_includes=source_location_include.abspath()
    )

    if bld.is_toplevel():
        bld.program(
            features="cxx test",
            source=["example/main.cpp"],
            target="source_location_tests",
            use=["source_location"],
        )
