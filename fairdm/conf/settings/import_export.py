from import_export.formats.base_formats import DEFAULT_FORMATS, CSV, TSV, XLS, XLSX, ODS
from fairdm.contrib.import_export.formats import LaTex

IMPORT_EXPORT_FORMATS = [LaTex, *DEFAULT_FORMATS]

IMPORT_FORMATS = [CSV, TSV, XLS, XLSX, ODS]
