load("@bazel_tools//tools/build_defs/repo:http.bzl", "http_archive")

http_archive(
    name = "rules_python",
    sha256 = "b86e332e135f32925137de74c335737f3a8e73354184883270b7b63c427a247c",
    strip_prefix = "rules_python-0.26.0",
    url = "https://github.com/bazelbuild/rules_python/releases/download/0.26.0/rules_python-0.26.0.tar.gz",
)

load("@rules_python//python:pip.bzl", "pip_install")

pip_install(
   name = "pip_dependencies",
   requirements = "//:requirements.txt",
)
