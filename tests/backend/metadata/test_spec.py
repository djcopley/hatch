import pytest

from hatchling.metadata.core import ProjectMetadata
from hatchling.metadata.spec import (
    LATEST_METADATA_VERSION,
    get_core_metadata_constructors,
    project_metadata_from_core_metadata,
)


class TestProjectMetadataFromCoreMetadata:
    def test_missing_name(self):
        core_metadata = f"""\
Metadata-Version: {LATEST_METADATA_VERSION}
"""
        with pytest.raises(ValueError, match='^Missing required core metadata: Name$'):
            project_metadata_from_core_metadata(core_metadata)

    def test_missing_version(self):
        core_metadata = f"""\
Metadata-Version: {LATEST_METADATA_VERSION}
Name: My.App
"""
        with pytest.raises(ValueError, match='^Missing required core metadata: Version$'):
            project_metadata_from_core_metadata(core_metadata)

    def test_dynamic(self):
        core_metadata = f"""\
Metadata-Version: {LATEST_METADATA_VERSION}
Name: My.App
Version: 0.1.0
Dynamic: Classifier
Dynamic: Provides-Extra
"""
        assert project_metadata_from_core_metadata(core_metadata) == {
            'name': 'My.App',
            'version': '0.1.0',
            'dynamic': ['classifiers', 'dependencies', 'optional-dependencies'],
        }

    def test_description(self):
        core_metadata = f"""\
Metadata-Version: {LATEST_METADATA_VERSION}
Name: My.App
Version: 0.1.0
Summary: foo
"""
        assert project_metadata_from_core_metadata(core_metadata) == {
            'name': 'My.App',
            'version': '0.1.0',
            'description': 'foo',
        }

    def test_urls(self):
        core_metadata = f"""\
Metadata-Version: {LATEST_METADATA_VERSION}
Name: My.App
Version: 0.1.0
Project-URL: foo, bar
Project-URL: bar, baz
"""
        assert project_metadata_from_core_metadata(core_metadata) == {
            'name': 'My.App',
            'version': '0.1.0',
            'urls': {'foo': 'bar', 'bar': 'baz'},
        }

    def test_authors(self):
        core_metadata = f"""\
Metadata-Version: {LATEST_METADATA_VERSION}
Name: My.App
Version: 0.1.0
Author: foobar
Author-email: foo <bar@domain>, <baz@domain>
"""
        assert project_metadata_from_core_metadata(core_metadata) == {
            'name': 'My.App',
            'version': '0.1.0',
            'authors': [{'name': 'foobar'}, {'email': 'bar@domain', 'name': 'foo'}, {'email': 'baz@domain'}],
        }

    def test_maintainers(self):
        core_metadata = f"""\
Metadata-Version: {LATEST_METADATA_VERSION}
Name: My.App
Version: 0.1.0
Maintainer: foobar
Maintainer-email: foo <bar@domain>, <baz@domain>
"""
        assert project_metadata_from_core_metadata(core_metadata) == {
            'name': 'My.App',
            'version': '0.1.0',
            'maintainers': [{'name': 'foobar'}, {'email': 'bar@domain', 'name': 'foo'}, {'email': 'baz@domain'}],
        }

    def test_keywords(self):
        core_metadata = f"""\
Metadata-Version: {LATEST_METADATA_VERSION}
Name: My.App
Version: 0.1.0
Keywords: bar,foo
"""
        assert project_metadata_from_core_metadata(core_metadata) == {
            'name': 'My.App',
            'version': '0.1.0',
            'keywords': ['bar', 'foo'],
        }

    def test_classifiers(self):
        core_metadata = f"""\
Metadata-Version: {LATEST_METADATA_VERSION}
Name: My.App
Version: 0.1.0
Classifier: Programming Language :: Python :: 3.9
Classifier: Programming Language :: Python :: 3.11
"""
        assert project_metadata_from_core_metadata(core_metadata) == {
            'name': 'My.App',
            'version': '0.1.0',
            'classifiers': ['Programming Language :: Python :: 3.9', 'Programming Language :: Python :: 3.11'],
        }

    def test_license_files(self):
        core_metadata = f"""\
Metadata-Version: {LATEST_METADATA_VERSION}
Name: My.App
Version: 0.1.0
License-File: LICENSES/Apache-2.0.txt
License-File: LICENSES/MIT.txt
"""
        assert project_metadata_from_core_metadata(core_metadata) == {
            'name': 'My.App',
            'version': '0.1.0',
            'license-files': ['LICENSES/Apache-2.0.txt', 'LICENSES/MIT.txt'],
        }

    def test_license_expression(self):
        core_metadata = f"""\
Metadata-Version: {LATEST_METADATA_VERSION}
Name: My.App
Version: 0.1.0
License-Expression: MIT
"""
        assert project_metadata_from_core_metadata(core_metadata) == {
            'name': 'My.App',
            'version': '0.1.0',
            'license': 'MIT',
        }

    def test_license_legacy(self):
        core_metadata = f"""\
Metadata-Version: {LATEST_METADATA_VERSION}
Name: My.App
Version: 0.1.0
License: foo
"""
        assert project_metadata_from_core_metadata(core_metadata) == {
            'name': 'My.App',
            'version': '0.1.0',
            'license': {'text': 'foo'},
        }

    def test_readme(self):
        core_metadata = f"""\
Metadata-Version: {LATEST_METADATA_VERSION}
Name: My.App
Version: 0.1.0
Description-Content-Type: text/markdown

test content
"""
        assert project_metadata_from_core_metadata(core_metadata) == {
            'name': 'My.App',
            'version': '0.1.0',
            'readme': {'content-type': 'text/markdown', 'text': 'test content\n'},
        }

    def test_readme_default_content_type(self):
        core_metadata = f"""\
Metadata-Version: {LATEST_METADATA_VERSION}
Name: My.App
Version: 0.1.0

test content
"""
        assert project_metadata_from_core_metadata(core_metadata) == {
            'name': 'My.App',
            'version': '0.1.0',
            'readme': {'content-type': 'text/plain', 'text': 'test content\n'},
        }

    def test_requires_python(self):
        core_metadata = f"""\
Metadata-Version: {LATEST_METADATA_VERSION}
Name: My.App
Version: 0.1.0
Requires-Python: <2,>=1
"""
        assert project_metadata_from_core_metadata(core_metadata) == {
            'name': 'My.App',
            'version': '0.1.0',
            'requires-python': '<2,>=1',
        }

    def test_dependencies(self):
        core_metadata = f"""\
Metadata-Version: {LATEST_METADATA_VERSION}
Name: My.App
Version: 0.1.0
Requires-Dist: bar==5
Requires-Dist: foo==1
Provides-Extra: feature1
Requires-Dist: bar==5; (python_version < '3') and extra == 'feature1'
Requires-Dist: foo==1; extra == 'feature1'
Provides-Extra: feature2
Requires-Dist: bar==5; extra == 'feature2'
Requires-Dist: foo==1; (python_version < '3') and extra == 'feature2'
Provides-Extra: feature3
Requires-Dist: baz@ file:///path/to/project ; extra == 'feature3'
"""
        assert project_metadata_from_core_metadata(core_metadata) == {
            'name': 'My.App',
            'version': '0.1.0',
            'dependencies': ['bar==5', 'foo==1'],
            'optional-dependencies': {
                'feature1': ['bar==5; python_version < "3"', 'foo==1'],
                'feature2': ['bar==5', 'foo==1; python_version < "3"'],
                'feature3': ['baz@ file:///path/to/project'],
            },
        }


@pytest.mark.parametrize('constructor', [get_core_metadata_constructors()['1.2']])
class TestCoreMetadataV12:
    def test_default(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0'}})

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            """
        )

    def test_description(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'description': 'foo'}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            Summary: foo
            """
        )

    def test_urls(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'urls': {'foo': 'bar', 'bar': 'baz'}}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            Project-URL: foo, bar
            Project-URL: bar, baz
            """
        )

    def test_authors_name(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'name': 'foo'}]}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            Author: foo
            """
        )

    def test_authors_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'email': 'foo@domain'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            Author-email: foo@domain
            """
        )

    def test_authors_name_and_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'email': 'bar@domain', 'name': 'foo'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            Author-email: foo <bar@domain>
            """
        )

    def test_authors_multiple(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'name': 'foo'}, {'name': 'bar'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            Author: foo, bar
            """
        )

    def test_maintainers_name(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'maintainers': [{'name': 'foo'}]}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            Maintainer: foo
            """
        )

    def test_maintainers_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'maintainers': [{'email': 'foo@domain'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            Maintainer-email: foo@domain
            """
        )

    def test_maintainers_name_and_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {
                'project': {
                    'name': 'My.App',
                    'version': '0.1.0',
                    'maintainers': [{'email': 'bar@domain', 'name': 'foo'}],
                }
            },
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            Maintainer-email: foo <bar@domain>
            """
        )

    def test_maintainers_multiple(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'maintainers': [{'name': 'foo'}, {'name': 'bar'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            Maintainer: foo, bar
            """
        )

    def test_license(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'license': {'text': 'foo\nbar'}}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            License: foo
                    bar
            """
        )

    def test_license_expression(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'license': 'mit'}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            License: MIT
            """
        )

    def test_keywords_single(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'keywords': ['foo']}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            Keywords: foo
            """
        )

    def test_keywords_multiple(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'keywords': ['foo', 'bar']}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            Keywords: bar,foo
            """
        )

    def test_classifiers(self, constructor, isolation, helpers):
        classifiers = [
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.9',
        ]
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'classifiers': classifiers}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            Classifier: Programming Language :: Python :: 3.9
            Classifier: Programming Language :: Python :: 3.11
            """
        )

    def test_requires_python(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'requires-python': '>=1,<2'}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            Requires-Python: <2,>=1
            """
        )

    def test_dependencies(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'dependencies': ['foo==1', 'bar==5']}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            Requires-Dist: bar==5
            Requires-Dist: foo==1
            """
        )

    def test_extra_runtime_dependencies(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'dependencies': ['foo==1', 'bar==5']}},
        )

        assert constructor(metadata, extra_dependencies=['baz==9']) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            Requires-Dist: bar==5
            Requires-Dist: foo==1
            Requires-Dist: baz==9
            """
        )

    def test_all(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {
                'project': {
                    'name': 'My.App',
                    'version': '0.1.0',
                    'description': 'foo',
                    'urls': {'foo': 'bar', 'bar': 'baz'},
                    'authors': [{'email': 'bar@domain', 'name': 'foo'}],
                    'maintainers': [{'email': 'bar@domain', 'name': 'foo'}],
                    'license': {'text': 'foo\nbar'},
                    'keywords': ['foo', 'bar'],
                    'classifiers': [
                        'Programming Language :: Python :: 3.11',
                        'Programming Language :: Python :: 3.9',
                    ],
                    'requires-python': '>=1,<2',
                    'dependencies': ['foo==1', 'bar==5'],
                }
            },
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 1.2
            Name: My.App
            Version: 0.1.0
            Summary: foo
            Project-URL: foo, bar
            Project-URL: bar, baz
            Author-email: foo <bar@domain>
            Maintainer-email: foo <bar@domain>
            License: foo
                    bar
            Keywords: bar,foo
            Classifier: Programming Language :: Python :: 3.9
            Classifier: Programming Language :: Python :: 3.11
            Requires-Python: <2,>=1
            Requires-Dist: bar==5
            Requires-Dist: foo==1
            """
        )


@pytest.mark.parametrize('constructor', [get_core_metadata_constructors()['2.1']])
class TestCoreMetadataV21:
    def test_default(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0'}})

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            """
        )

    def test_description(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'description': 'foo'}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            Summary: foo
            """
        )

    def test_urls(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'urls': {'foo': 'bar', 'bar': 'baz'}}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            Project-URL: foo, bar
            Project-URL: bar, baz
            """
        )

    def test_authors_name(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'name': 'foo'}]}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            Author: foo
            """
        )

    def test_authors_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'email': 'foo@domain'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            Author-email: foo@domain
            """
        )

    def test_authors_name_and_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'email': 'bar@domain', 'name': 'foo'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            Author-email: foo <bar@domain>
            """
        )

    def test_authors_multiple(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'name': 'foo'}, {'name': 'bar'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            Author: foo, bar
            """
        )

    def test_maintainers_name(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'maintainers': [{'name': 'foo'}]}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            Maintainer: foo
            """
        )

    def test_maintainers_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'maintainers': [{'email': 'foo@domain'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            Maintainer-email: foo@domain
            """
        )

    def test_maintainers_name_and_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {
                'project': {
                    'name': 'My.App',
                    'version': '0.1.0',
                    'maintainers': [{'email': 'bar@domain', 'name': 'foo'}],
                }
            },
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            Maintainer-email: foo <bar@domain>
            """
        )

    def test_maintainers_multiple(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'maintainers': [{'name': 'foo'}, {'name': 'bar'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            Maintainer: foo, bar
            """
        )

    def test_license(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'license': {'text': 'foo\nbar'}}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            License: foo
                    bar
            """
        )

    def test_license_expression(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'license': 'mit'}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            License: MIT
            """
        )

    def test_keywords_single(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'keywords': ['foo']}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            Keywords: foo
            """
        )

    def test_keywords_multiple(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'keywords': ['foo', 'bar']}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            Keywords: bar,foo
            """
        )

    def test_classifiers(self, constructor, isolation, helpers):
        classifiers = [
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.9',
        ]
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'classifiers': classifiers}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            Classifier: Programming Language :: Python :: 3.9
            Classifier: Programming Language :: Python :: 3.11
            """
        )

    def test_requires_python(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'requires-python': '>=1,<2'}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            Requires-Python: <2,>=1
            """
        )

    def test_dependencies(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'dependencies': ['foo==1', 'bar==5']}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            Requires-Dist: bar==5
            Requires-Dist: foo==1
            """
        )

    def test_optional_dependencies(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {
                'project': {
                    'name': 'My.App',
                    'version': '0.1.0',
                    'optional-dependencies': {
                        'feature2': ['foo==1; python_version < "3"', 'bar==5'],
                        'feature1': ['foo==1', 'bar==5; python_version < "3"'],
                    },
                }
            },
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            Provides-Extra: feature1
            Requires-Dist: bar==5; (python_version < '3') and extra == 'feature1'
            Requires-Dist: foo==1; extra == 'feature1'
            Provides-Extra: feature2
            Requires-Dist: bar==5; extra == 'feature2'
            Requires-Dist: foo==1; (python_version < '3') and extra == 'feature2'
            """
        )

    def test_extra_runtime_dependencies(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'dependencies': ['foo==1', 'bar==5']}},
        )

        assert constructor(metadata, extra_dependencies=['baz==9']) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            Requires-Dist: bar==5
            Requires-Dist: foo==1
            Requires-Dist: baz==9
            """
        )

    def test_readme(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {
                'project': {
                    'name': 'My.App',
                    'version': '0.1.0',
                    'readme': {'content-type': 'text/markdown', 'text': 'test content\n'},
                }
            },
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            Description-Content-Type: text/markdown

            test content
            """
        )

    def test_all(self, constructor, helpers, temp_dir):
        metadata = ProjectMetadata(
            str(temp_dir),
            None,
            {
                'project': {
                    'name': 'My.App',
                    'version': '0.1.0',
                    'description': 'foo',
                    'urls': {'foo': 'bar', 'bar': 'baz'},
                    'authors': [{'email': 'bar@domain', 'name': 'foo'}],
                    'maintainers': [{'email': 'bar@domain', 'name': 'foo'}],
                    'license': {'text': 'foo\nbar'},
                    'keywords': ['foo', 'bar'],
                    'classifiers': [
                        'Programming Language :: Python :: 3.11',
                        'Programming Language :: Python :: 3.9',
                    ],
                    'requires-python': '>=1,<2',
                    'dependencies': ['foo==1', 'bar==5'],
                    'optional-dependencies': {
                        'feature2': ['foo==1; python_version < "3"', 'bar==5'],
                        'feature1': ['foo==1', 'bar==5; python_version < "3"'],
                        'feature3': ['baz @ file:///path/to/project'],
                    },
                    'readme': {'content-type': 'text/markdown', 'text': 'test content\n'},
                },
                'tool': {'hatch': {'metadata': {'allow-direct-references': True}}},
            },
        )

        (temp_dir / 'LICENSE.txt').touch()

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.1
            Name: My.App
            Version: 0.1.0
            Summary: foo
            Project-URL: foo, bar
            Project-URL: bar, baz
            Author-email: foo <bar@domain>
            Maintainer-email: foo <bar@domain>
            License: foo
                    bar
            Keywords: bar,foo
            Classifier: Programming Language :: Python :: 3.9
            Classifier: Programming Language :: Python :: 3.11
            Requires-Python: <2,>=1
            Requires-Dist: bar==5
            Requires-Dist: foo==1
            Provides-Extra: feature1
            Requires-Dist: bar==5; (python_version < '3') and extra == 'feature1'
            Requires-Dist: foo==1; extra == 'feature1'
            Provides-Extra: feature2
            Requires-Dist: bar==5; extra == 'feature2'
            Requires-Dist: foo==1; (python_version < '3') and extra == 'feature2'
            Provides-Extra: feature3
            Requires-Dist: baz@ file:///path/to/project ; extra == 'feature3'
            Description-Content-Type: text/markdown

            test content
            """
        )


@pytest.mark.parametrize('constructor', [get_core_metadata_constructors()['2.2']])
class TestCoreMetadataV22:
    def test_default(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0'}})

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            """
        )

    def test_dynamic(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'dynamic': ['authors', 'classifiers']}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Dynamic: Author
            Dynamic: Author-email
            Dynamic: Classifier
            """
        )

    def test_description(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'description': 'foo'}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Summary: foo
            """
        )

    def test_urls(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'urls': {'foo': 'bar', 'bar': 'baz'}}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Project-URL: foo, bar
            Project-URL: bar, baz
            """
        )

    def test_authors_name(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'name': 'foo'}]}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Author: foo
            """
        )

    def test_authors_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'email': 'foo@domain'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Author-email: foo@domain
            """
        )

    def test_authors_name_and_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'email': 'bar@domain', 'name': 'foo'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Author-email: foo <bar@domain>
            """
        )

    def test_authors_multiple(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'name': 'foo'}, {'name': 'bar'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Author: foo, bar
            """
        )

    def test_maintainers_name(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'maintainers': [{'name': 'foo'}]}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Maintainer: foo
            """
        )

    def test_maintainers_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'maintainers': [{'email': 'foo@domain'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Maintainer-email: foo@domain
            """
        )

    def test_maintainers_name_and_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {
                'project': {
                    'name': 'My.App',
                    'version': '0.1.0',
                    'maintainers': [{'email': 'bar@domain', 'name': 'foo'}],
                }
            },
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Maintainer-email: foo <bar@domain>
            """
        )

    def test_maintainers_multiple(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'maintainers': [{'name': 'foo'}, {'name': 'bar'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Maintainer: foo, bar
            """
        )

    def test_license(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'license': {'text': 'foo\nbar'}}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            License: foo
                    bar
            """
        )

    def test_license_expression(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'license': 'mit'}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            License: MIT
            """
        )

    def test_keywords_single(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'keywords': ['foo']}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Keywords: foo
            """
        )

    def test_keywords_multiple(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'keywords': ['foo', 'bar']}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Keywords: bar,foo
            """
        )

    def test_classifiers(self, constructor, isolation, helpers):
        classifiers = [
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.9',
        ]
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'classifiers': classifiers}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Classifier: Programming Language :: Python :: 3.9
            Classifier: Programming Language :: Python :: 3.11
            """
        )

    def test_requires_python(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'requires-python': '>=1,<2'}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Requires-Python: <2,>=1
            """
        )

    def test_dependencies(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'dependencies': ['foo==1', 'bar==5']}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Requires-Dist: bar==5
            Requires-Dist: foo==1
            """
        )

    def test_optional_dependencies(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {
                'project': {
                    'name': 'My.App',
                    'version': '0.1.0',
                    'optional-dependencies': {
                        'feature2': ['foo==1; python_version < "3"', 'bar==5'],
                        'feature1': ['foo==1', 'bar==5; python_version < "3"'],
                    },
                }
            },
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Provides-Extra: feature1
            Requires-Dist: bar==5; (python_version < '3') and extra == 'feature1'
            Requires-Dist: foo==1; extra == 'feature1'
            Provides-Extra: feature2
            Requires-Dist: bar==5; extra == 'feature2'
            Requires-Dist: foo==1; (python_version < '3') and extra == 'feature2'
            """
        )

    def test_optional_complex_dependencies(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {
                'project': {
                    'name': 'My.App',
                    'version': '0.1.0',
                    'optional-dependencies': {
                        'feature2': ['foo==1; sys_platform == "win32" or python_version < "3"', 'bar==5'],
                        'feature1': ['foo==1', 'bar==5; python_version < "3"'],
                    },
                }
            },
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Provides-Extra: feature1
            Requires-Dist: bar==5; (python_version < '3') and extra == 'feature1'
            Requires-Dist: foo==1; extra == 'feature1'
            Provides-Extra: feature2
            Requires-Dist: bar==5; extra == 'feature2'
            Requires-Dist: foo==1; (sys_platform == 'win32' or python_version < '3') and extra == 'feature2'
            """
        )

    def test_extra_runtime_dependencies(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'dependencies': ['foo==1', 'bar==5']}},
        )

        assert constructor(metadata, extra_dependencies=['baz==9']) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Requires-Dist: bar==5
            Requires-Dist: foo==1
            Requires-Dist: baz==9
            """
        )

    def test_readme(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {
                'project': {
                    'name': 'My.App',
                    'version': '0.1.0',
                    'readme': {'content-type': 'text/markdown', 'text': 'test content\n'},
                }
            },
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Description-Content-Type: text/markdown

            test content
            """
        )

    def test_all(self, constructor, helpers, temp_dir):
        metadata = ProjectMetadata(
            str(temp_dir),
            None,
            {
                'project': {
                    'name': 'My.App',
                    'version': '0.1.0',
                    'description': 'foo',
                    'urls': {'foo': 'bar', 'bar': 'baz'},
                    'authors': [{'email': 'bar@domain', 'name': 'foo'}],
                    'maintainers': [{'email': 'bar@domain', 'name': 'foo'}],
                    'license': {'text': 'foo\nbar'},
                    'keywords': ['foo', 'bar'],
                    'classifiers': [
                        'Programming Language :: Python :: 3.11',
                        'Programming Language :: Python :: 3.9',
                    ],
                    'requires-python': '>=1,<2',
                    'dependencies': ['foo==1', 'bar==5'],
                    'optional-dependencies': {
                        'feature2': ['foo==1; python_version < "3"', 'bar==5'],
                        'feature1': ['foo==1', 'bar==5; python_version < "3"'],
                        'feature3': ['baz @ file:///path/to/project'],
                    },
                    'readme': {'content-type': 'text/markdown', 'text': 'test content\n'},
                },
                'tool': {'hatch': {'metadata': {'allow-direct-references': True}}},
            },
        )

        (temp_dir / 'LICENSE.txt').touch()

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.2
            Name: My.App
            Version: 0.1.0
            Summary: foo
            Project-URL: foo, bar
            Project-URL: bar, baz
            Author-email: foo <bar@domain>
            Maintainer-email: foo <bar@domain>
            License: foo
                    bar
            Keywords: bar,foo
            Classifier: Programming Language :: Python :: 3.9
            Classifier: Programming Language :: Python :: 3.11
            Requires-Python: <2,>=1
            Requires-Dist: bar==5
            Requires-Dist: foo==1
            Provides-Extra: feature1
            Requires-Dist: bar==5; (python_version < '3') and extra == 'feature1'
            Requires-Dist: foo==1; extra == 'feature1'
            Provides-Extra: feature2
            Requires-Dist: bar==5; extra == 'feature2'
            Requires-Dist: foo==1; (python_version < '3') and extra == 'feature2'
            Provides-Extra: feature3
            Requires-Dist: baz@ file:///path/to/project ; extra == 'feature3'
            Description-Content-Type: text/markdown

            test content
            """
        )


@pytest.mark.parametrize('constructor', [get_core_metadata_constructors()['2.3']])
class TestCoreMetadataV23:
    def test_default(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0'}})

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            """
        )

    def test_description(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'description': 'foo'}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Summary: foo
            """
        )

    def test_dynamic(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'dynamic': ['authors', 'classifiers']}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Dynamic: Author
            Dynamic: Author-email
            Dynamic: Classifier
            """
        )

    def test_urls(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'urls': {'foo': 'bar', 'bar': 'baz'}}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Project-URL: foo, bar
            Project-URL: bar, baz
            """
        )

    def test_authors_name(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'name': 'foo'}]}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Author: foo
            """
        )

    def test_authors_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'email': 'foo@domain'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Author-email: foo@domain
            """
        )

    def test_authors_name_and_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'email': 'bar@domain', 'name': 'foo'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Author-email: foo <bar@domain>
            """
        )

    def test_authors_multiple(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'name': 'foo'}, {'name': 'bar'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Author: foo, bar
            """
        )

    def test_maintainers_name(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'maintainers': [{'name': 'foo'}]}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Maintainer: foo
            """
        )

    def test_maintainers_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'maintainers': [{'email': 'foo@domain'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Maintainer-email: foo@domain
            """
        )

    def test_maintainers_name_and_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {
                'project': {
                    'name': 'My.App',
                    'version': '0.1.0',
                    'maintainers': [{'email': 'bar@domain', 'name': 'foo'}],
                }
            },
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Maintainer-email: foo <bar@domain>
            """
        )

    def test_maintainers_multiple(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'maintainers': [{'name': 'foo'}, {'name': 'bar'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Maintainer: foo, bar
            """
        )

    def test_license(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'license': {'text': 'foo\nbar'}}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            License: foo
                    bar
            """
        )

    def test_license_expression(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'license': 'mit'}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            License: MIT
            """
        )

    def test_keywords_single(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'keywords': ['foo']}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Keywords: foo
            """
        )

    def test_keywords_multiple(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'keywords': ['foo', 'bar']}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Keywords: bar,foo
            """
        )

    def test_classifiers(self, constructor, isolation, helpers):
        classifiers = [
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.9',
        ]
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'classifiers': classifiers}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Classifier: Programming Language :: Python :: 3.9
            Classifier: Programming Language :: Python :: 3.11
            """
        )

    def test_requires_python(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'requires-python': '>=1,<2'}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Requires-Python: <2,>=1
            """
        )

    def test_dependencies(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'dependencies': ['foo==1', 'bar==5']}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Requires-Dist: bar==5
            Requires-Dist: foo==1
            """
        )

    def test_optional_dependencies(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {
                'project': {
                    'name': 'My.App',
                    'version': '0.1.0',
                    'optional-dependencies': {
                        'feature2': ['foo==1; python_version < "3"', 'bar==5'],
                        'feature1': ['foo==1', 'bar==5; python_version < "3"'],
                    },
                }
            },
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Provides-Extra: feature1
            Requires-Dist: bar==5; (python_version < '3') and extra == 'feature1'
            Requires-Dist: foo==1; extra == 'feature1'
            Provides-Extra: feature2
            Requires-Dist: bar==5; extra == 'feature2'
            Requires-Dist: foo==1; (python_version < '3') and extra == 'feature2'
            """
        )

    def test_extra_runtime_dependencies(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'dependencies': ['foo==1', 'bar==5']}},
        )

        assert constructor(metadata, extra_dependencies=['baz==9']) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Requires-Dist: bar==5
            Requires-Dist: foo==1
            Requires-Dist: baz==9
            """
        )

    def test_readme(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {
                'project': {
                    'name': 'My.App',
                    'version': '0.1.0',
                    'readme': {'content-type': 'text/markdown', 'text': 'test content\n'},
                }
            },
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Description-Content-Type: text/markdown

            test content
            """
        )

    def test_all(self, constructor, temp_dir, helpers):
        metadata = ProjectMetadata(
            str(temp_dir),
            None,
            {
                'project': {
                    'name': 'My.App',
                    'version': '0.1.0',
                    'description': 'foo',
                    'urls': {'foo': 'bar', 'bar': 'baz'},
                    'authors': [{'email': 'bar@domain', 'name': 'foo'}],
                    'maintainers': [{'email': 'bar@domain', 'name': 'foo'}],
                    'keywords': ['foo', 'bar'],
                    'classifiers': [
                        'Programming Language :: Python :: 3.11',
                        'Programming Language :: Python :: 3.9',
                    ],
                    'requires-python': '>=1,<2',
                    'dependencies': ['foo==1', 'bar==5'],
                    'optional-dependencies': {
                        'feature2': ['foo==1; python_version < "3"', 'bar==5'],
                        'feature1': ['foo==1', 'bar==5; python_version < "3"'],
                        'feature3': ['baz @ file:///path/to/project'],
                    },
                    'readme': {'content-type': 'text/markdown', 'text': 'test content\n'},
                },
                'tool': {'hatch': {'metadata': {'allow-direct-references': True}}},
            },
        )

        licenses_dir = temp_dir / 'LICENSES'
        licenses_dir.mkdir()
        (licenses_dir / 'MIT.txt').touch()
        (licenses_dir / 'Apache-2.0.txt').touch()

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.3
            Name: My.App
            Version: 0.1.0
            Summary: foo
            Project-URL: foo, bar
            Project-URL: bar, baz
            Author-email: foo <bar@domain>
            Maintainer-email: foo <bar@domain>
            Keywords: bar,foo
            Classifier: Programming Language :: Python :: 3.9
            Classifier: Programming Language :: Python :: 3.11
            Requires-Python: <2,>=1
            Requires-Dist: bar==5
            Requires-Dist: foo==1
            Provides-Extra: feature1
            Requires-Dist: bar==5; (python_version < '3') and extra == 'feature1'
            Requires-Dist: foo==1; extra == 'feature1'
            Provides-Extra: feature2
            Requires-Dist: bar==5; extra == 'feature2'
            Requires-Dist: foo==1; (python_version < '3') and extra == 'feature2'
            Provides-Extra: feature3
            Requires-Dist: baz@ file:///path/to/project ; extra == 'feature3'
            Description-Content-Type: text/markdown

            test content
            """
        )


@pytest.mark.parametrize('constructor', [get_core_metadata_constructors()['2.4']])
class TestCoreMetadataV24:
    def test_default(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0'}})

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            """
        )

    def test_description(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'description': 'foo'}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Summary: foo
            """
        )

    def test_dynamic(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'dynamic': ['authors', 'classifiers']}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Dynamic: Author
            Dynamic: Author-email
            Dynamic: Classifier
            """
        )

    def test_urls(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'urls': {'foo': 'bar', 'bar': 'baz'}}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Project-URL: foo, bar
            Project-URL: bar, baz
            """
        )

    def test_authors_name(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'name': 'foo'}]}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Author: foo
            """
        )

    def test_authors_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'email': 'foo@domain'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Author-email: foo@domain
            """
        )

    def test_authors_name_and_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'email': 'bar@domain', 'name': 'foo'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Author-email: foo <bar@domain>
            """
        )

    def test_authors_multiple(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'authors': [{'name': 'foo'}, {'name': 'bar'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Author: foo, bar
            """
        )

    def test_maintainers_name(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'maintainers': [{'name': 'foo'}]}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Maintainer: foo
            """
        )

    def test_maintainers_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'maintainers': [{'email': 'foo@domain'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Maintainer-email: foo@domain
            """
        )

    def test_maintainers_name_and_email(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {
                'project': {
                    'name': 'My.App',
                    'version': '0.1.0',
                    'maintainers': [{'email': 'bar@domain', 'name': 'foo'}],
                }
            },
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Maintainer-email: foo <bar@domain>
            """
        )

    def test_maintainers_multiple(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'maintainers': [{'name': 'foo'}, {'name': 'bar'}]}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Maintainer: foo, bar
            """
        )

    def test_license(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'license': {'text': 'foo\nbar'}}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            License: foo
                    bar
            """
        )

    def test_license_expression(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'license': 'mit or apache-2.0'}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            License-Expression: MIT OR Apache-2.0
            """
        )

    def test_license_files(self, constructor, temp_dir, helpers):
        metadata = ProjectMetadata(
            str(temp_dir),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'license-files': ['LICENSES/*']}},
        )

        licenses_dir = temp_dir / 'LICENSES'
        licenses_dir.mkdir()
        (licenses_dir / 'MIT.txt').touch()
        (licenses_dir / 'Apache-2.0.txt').touch()

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            License-File: LICENSES/Apache-2.0.txt
            License-File: LICENSES/MIT.txt
            """
        )

    def test_keywords_single(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'keywords': ['foo']}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Keywords: foo
            """
        )

    def test_keywords_multiple(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'keywords': ['foo', 'bar']}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Keywords: bar,foo
            """
        )

    def test_classifiers(self, constructor, isolation, helpers):
        classifiers = [
            'Programming Language :: Python :: 3.11',
            'Programming Language :: Python :: 3.9',
        ]
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'classifiers': classifiers}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Classifier: Programming Language :: Python :: 3.9
            Classifier: Programming Language :: Python :: 3.11
            """
        )

    def test_requires_python(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation), None, {'project': {'name': 'My.App', 'version': '0.1.0', 'requires-python': '>=1,<2'}}
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Requires-Python: <2,>=1
            """
        )

    def test_dependencies(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'dependencies': ['foo==1', 'bar==5']}},
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Requires-Dist: bar==5
            Requires-Dist: foo==1
            """
        )

    def test_optional_dependencies(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {
                'project': {
                    'name': 'My.App',
                    'version': '0.1.0',
                    'optional-dependencies': {
                        'feature2': ['foo==1; python_version < "3"', 'bar==5'],
                        'feature1': ['foo==1', 'bar==5; python_version < "3"'],
                    },
                }
            },
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Provides-Extra: feature1
            Requires-Dist: bar==5; (python_version < '3') and extra == 'feature1'
            Requires-Dist: foo==1; extra == 'feature1'
            Provides-Extra: feature2
            Requires-Dist: bar==5; extra == 'feature2'
            Requires-Dist: foo==1; (python_version < '3') and extra == 'feature2'
            """
        )

    def test_extra_runtime_dependencies(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {'project': {'name': 'My.App', 'version': '0.1.0', 'dependencies': ['foo==1', 'bar==5']}},
        )

        assert constructor(metadata, extra_dependencies=['baz==9']) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Requires-Dist: bar==5
            Requires-Dist: foo==1
            Requires-Dist: baz==9
            """
        )

    def test_readme(self, constructor, isolation, helpers):
        metadata = ProjectMetadata(
            str(isolation),
            None,
            {
                'project': {
                    'name': 'My.App',
                    'version': '0.1.0',
                    'readme': {'content-type': 'text/markdown', 'text': 'test content\n'},
                }
            },
        )

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Description-Content-Type: text/markdown

            test content
            """
        )

    def test_all(self, constructor, temp_dir, helpers):
        metadata = ProjectMetadata(
            str(temp_dir),
            None,
            {
                'project': {
                    'name': 'My.App',
                    'version': '0.1.0',
                    'description': 'foo',
                    'urls': {'foo': 'bar', 'bar': 'baz'},
                    'authors': [{'email': 'bar@domain', 'name': 'foo'}],
                    'maintainers': [{'email': 'bar@domain', 'name': 'foo'}],
                    'license': 'mit or apache-2.0',
                    'license-files': ['LICENSES/*'],
                    'keywords': ['foo', 'bar'],
                    'classifiers': [
                        'Programming Language :: Python :: 3.11',
                        'Programming Language :: Python :: 3.9',
                    ],
                    'requires-python': '>=1,<2',
                    'dependencies': ['foo==1', 'bar==5'],
                    'optional-dependencies': {
                        'feature2': ['foo==1; python_version < "3"', 'bar==5'],
                        'feature1': ['foo==1', 'bar==5; python_version < "3"'],
                        'feature3': ['baz @ file:///path/to/project'],
                    },
                    'readme': {'content-type': 'text/markdown', 'text': 'test content\n'},
                },
                'tool': {'hatch': {'metadata': {'allow-direct-references': True}}},
            },
        )

        licenses_dir = temp_dir / 'LICENSES'
        licenses_dir.mkdir()
        (licenses_dir / 'MIT.txt').touch()
        (licenses_dir / 'Apache-2.0.txt').touch()

        assert constructor(metadata) == helpers.dedent(
            """
            Metadata-Version: 2.4
            Name: My.App
            Version: 0.1.0
            Summary: foo
            Project-URL: foo, bar
            Project-URL: bar, baz
            Author-email: foo <bar@domain>
            Maintainer-email: foo <bar@domain>
            License-Expression: MIT OR Apache-2.0
            License-File: LICENSES/Apache-2.0.txt
            License-File: LICENSES/MIT.txt
            Keywords: bar,foo
            Classifier: Programming Language :: Python :: 3.9
            Classifier: Programming Language :: Python :: 3.11
            Requires-Python: <2,>=1
            Requires-Dist: bar==5
            Requires-Dist: foo==1
            Provides-Extra: feature1
            Requires-Dist: bar==5; (python_version < '3') and extra == 'feature1'
            Requires-Dist: foo==1; extra == 'feature1'
            Provides-Extra: feature2
            Requires-Dist: bar==5; extra == 'feature2'
            Requires-Dist: foo==1; (python_version < '3') and extra == 'feature2'
            Provides-Extra: feature3
            Requires-Dist: baz@ file:///path/to/project ; extra == 'feature3'
            Description-Content-Type: text/markdown

            test content
            """
        )
