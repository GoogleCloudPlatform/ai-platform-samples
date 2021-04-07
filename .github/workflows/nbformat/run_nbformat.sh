# Only check notebooks modified in this pull request.
notebooks="$(git diff --name-only master | grep '\.ipynb$' || true)"
if [[ -n "$notebooks" ]]; then
    echo "Check formatting with nbfmt:"
    python3 -m tensorflow_docs.tools.nbfmt --test "$notebooks"
else
    echo "No notebooks modified in this pull request."
fi