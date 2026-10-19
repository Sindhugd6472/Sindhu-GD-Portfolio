# Sample APB requirement

A transfer starts when PSEL is asserted.

PENABLE must be asserted in the access phase after the setup phase.

The transfer completes only when PREADY is high.

PSLVERR indicates an error response on a completing transfer.

This sample is intentionally small and is not a replacement for the official AMBA APB specification.
