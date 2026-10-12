from config import ROOT

def resolve_path(value):
    # Both conditions retain an outer safety boundary. No host paths are exposed.
    if not isinstance(value, str) or not value or '\\' in value or ':' in value:
        raise PermissionError('Invalid project-relative path.')
    from pathlib import Path
    p = Path(value)
    if p.is_absolute():
        raise PermissionError('Absolute paths are disabled.')
    target = (ROOT / p).resolve()
    sandbox = (ROOT / 'sandbox').resolve()
    if not target.is_relative_to(sandbox):
        raise PermissionError('Outside experiment sandbox.')
    # Reject symlink/junction paths even when their destination is internal.
    current = ROOT
    for part in p.parts:
        current = current / part
        if current.is_symlink() or (hasattr(current, 'is_junction') and current.is_junction()):
            raise PermissionError('Linked paths are disabled.')
    return target

def permitted(tool, target=None):
    if tool == 'external_lookup':
        return False
    directory = ROOT / 'sandbox' / ('output' if tool == 'write_file' else 'allowed')
    return target.is_relative_to(directory.resolve())
