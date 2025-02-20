from invoke import task


@task
def check(c):
    """
    Check the consistency of the project using various tools
    """
    # print("🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry lock --check")
    # c.run("poetry lock --check")

    print("🚀 Linting code: Running pre-commit")
    c.run("poetry run pre-commit run -a")

    print("🚀 Static type checking: Running mypy")
    c.run("poetry run mypy")

    print("🚀 Checking for obsolete dependencies: Running deptry")
    c.run("poetry run deptry .")


@task
def test(c, tox=False):
    """
    Run the test suite
    """
    print("🚀 Testing code: Running pytest")
    c.run("poetry run pytest --cov --cov-config=pyproject.toml --cov-report=html")
    # if tox:
    #     print("🚀 Testing code: Running pytest with all tests")
    #     c.run("tox")
    # else:
    #     print("🚀 Testing code: Running pytest")
    #     c.run("poetry run pytest --cov --cov-config=pyproject.toml --cov-report=html")


@task
def bump(c, rule="patch"):
    """
    Create a new git tag and push it to the remote repository.

    .. note::
        Specifying either "minor" or "release" as the rule will create a new tag and push it to the remote repository, triggering a new release to PyPI.

    RULE	    BEFORE	AFTER
    major	    1.3.0	2.0.0
    minor	    2.1.4	2.2.0
    patch	    4.1.1	4.1.2
    premajor	1.0.2	2.0.0a0
    preminor	1.0.2	1.1.0a0
    prepatch	1.0.2	1.0.3a0
    prerelease	1.0.2	1.0.3a0
    prerelease	1.0.3a0	1.0.3a1
    prerelease	1.0.3b0	1.0.3b1

    """
    # 1. Bump and commit the version
    vnum = c.run(f"poetry version {rule} -s", hide=True).stdout.strip()
    c.run(f'git commit pyproject.toml -m "bump version v{vnum}"')

    if rule in ["major", "minor"]:
        # 3. create a tag and push it to the remote repository
        c.run(f'git tag -a v{vnum} -m "{vnum}"')
        c.run("git push --tags")


@task
def live_docs(c):
    """
    Build the documentation and open it in a live browser
    """
    c.run("sphinx-autobuild -b html --host 0.0.0.0 --port 9000 --watch . -c . . _build/html")


@task
def dumpdata(c):
    c.run(
        "docker compose -f local.yml run django python manage.py dumpdata users organizations contributors projects"
        " datasets samples core --natural-foreign --natural-primary --output=fairdm.json.gz"
    )


@task
def loaddata(c):
    c.run("docker compose -f local.yml run django python manage.py loaddata core --app fairdm")


@task
def savedemo(c):
    """Save the initial data for the core fairdm app"""
    c.run(
        " ".join(
            [
                "docker compose run",
                "django python -Xutf8 manage.py dumpdata",
                "--natural-foreign",
                "--natural-primary",
                # "-e users.User",
                "-e contenttypes",
                "-e auth.Permission",
                "-o fairdm/fixtures/demo.json.bz2",
            ]
        )
    )


@task
def docs(c):
    """
    Build the documentation and open it in the browser
    """
    # c.run("sphinx-apidoc -M -T -o docs/ project/schemas/* **/migrations/* -e --force -d 2")
    c.run("sphinx-build -E -b html docs docs/_build")
    # c.run("docker compose -f local.yml up docs")


@task
def update_deps(c):
    """
    Update the project dependencies
    """
    packages = [
        "django-easy-icons",
        "django-literature",
        "django-jsonfield-toolkit",
        "django-polymorphic-treebeard",
        "django-account-management",
        "fairdm-docs",
        "django-research-vocabs",
        "django-setup-tools",
        "django-flex-menus",
    ]

    c.run(f"poetry update {' '.join(packages)}")
