# Changelog for akron ORM

## v0.2.4 (2025-09-28)
- **NEW**: Django-like foreign key syntax with `__foreign_keys__` class attribute
- **NEW**: Enhanced ModelMixin with `find_all()`, `get_by_id()`, `count()`, `exists()` methods
- **IMPROVED**: Better type handling for `Optional[Type]` fields in Pydantic models
- **IMPROVED**: Python 3.7+ typing compatibility with Union types
- **ADDED**: Comprehensive examples for Django-style foreign key usage
- **ADDED**: Type-safe foreign key relationships with automatic constraint creation
- **DOCS**: Updated README with Django-like foreign key examples

## v0.2.3 (2025-08-31)
- Schema management features
- Prisma-like `akron.json` configuration
- CLI improvements for modern schema workflows

## v0.1.0-alpha (2025-08-30)
- Initial release
- Universal ORM for SQLite, MySQL, PostgreSQL, MongoDB
- Simple dict and Pydantic model support
- Multi-table and foreign key support
- Auto migrations and CLI
- Typesafe models
- Basic error handling
- Pytest test coverage
