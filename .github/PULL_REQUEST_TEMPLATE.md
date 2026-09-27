## Summary

What does this change improve?

## Behavior affected

- [ ] Planning
- [ ] Classification
- [ ] Collision handling
- [ ] Organize/apply
- [ ] Rollback
- [ ] Manifest
- [ ] Undo
- [ ] Hashing
- [ ] CLI output
- [ ] Documentation / maintenance

## Validation

~~~bash
pytest -q
~~~

## Filesystem safety checklist

- [ ] The change does not silently overwrite user files.
- [ ] The change does not silently delete user files.
- [ ] Planning remains non-destructive.
- [ ] Changed behavior has tests where practical.
- [ ] Error/rollback behavior was considered.
- [ ] No personal files, credentials, or private paths are included.
