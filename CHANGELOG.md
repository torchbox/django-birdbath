# CHANGELOG

## Unreleased

- Add testing for Wagtail 6.3 & 7.0
- Use python 3.13 across workflows and formatting

## v2.0.1 (2024-10-22)

- Add tests
- Change project tooling to use ruff and flit
- Set up CI on GitHub
- Publish the source code on GitHub

## v2.0.0 (2024-04-17)

- Updates imports for compatibility with Wagtail >= 5.0, drops compatibility for older Wagtail releases

## v1.1.1 (2023-12-18)

- Remove upper bound on Faker dependency

## v1.1.0 (2023-02-20)

- Add black, flake8 and isort and fix all associated errors
- Actually use BIRDBATH_SKIP_CHECKS setting

## v1.0.0 (2022-07-05)

- Increase Faker version range
- Add default_auto_field, to silence Django 3.2 warning

## v0.0.5 (2021-06-10)

- Skip system check when running migrate management command

## v0.0.4 (2021-06-07)

- Improve compatibility with older Django versions

## v0.0.3 (2021-06-07)

- Update Faker version
- Remove un-used faker dependency
- Update README
- Add BaseModelAnonymiser class

## v0.0.2 (2022-09-07)

- Batch errors
- Add check for an 'ALLOWS_ANONYMISATION' variable
- Add configuration and Makefile for pypi
- Don't fail checks if birdbath tables don't exist
- Django system check if birdbath hasn't executed

## v0.0.1

Initial version
