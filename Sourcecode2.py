"""Small runner that delegates to the validated implementation in
`Sourcecode2_fixed.py`.

This file intentionally keeps only a thin wrapper so it cannot accidentally
contain duplicated or trailing content. The real implementation lives in
`Sourcecode2_fixed.py` which must be present in the same directory.
"""

import argparse

try:
    from Sourcecode2_fixed import main
except Exception as exc:
    raise RuntimeError("Sourcecode2_fixed.py must be present and importable") from exc


if __name__ == "__main__":
    # No seed CLI options anymore — the app seeds the full dataset automatically.
    main()
