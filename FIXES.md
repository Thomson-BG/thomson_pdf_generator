# Fixes

This document details the fixes made to the codebase.

## `seek of closed file` error in `core/pdf_handler.py`

The `get_pdf_info` method in `core/pdf_handler.py` was throwing a `seek of closed file` error because the file stream was being closed before it was accessed. This was fixed by opening the file in the `open_pdf` method and storing the file object. The file is now closed in the `close_pdf` method, which ensures that the file remains open while it is needed.

## `CryptographyDeprecationWarning` in `core/signer.py`

The `core/signer.py` module was throwing a `CryptographyDeprecationWarning` because the `not_valid_before` and `not_valid_after` methods were being used with naive datetime objects. This was fixed by using timezone-aware datetime objects and the `not_valid_before_utc` and `not_valid_after_utc` attributes when accessing the certificate's validity information.
