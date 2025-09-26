import pytest

from kikenda.exc import BadData
from kikenda.stages.base64 import Base64

parameterize_examples = pytest.mark.parametrize(
    "decoded,encoded",
    [(b"Hey", "SGV5"), (b"Hello", "SGVsbG8"), (b"Bonjour", "Qm9uam91cg")],
)


@parameterize_examples
def test_forward(decoded: bytes, encoded: str):
    assert Base64.forward(decoded) == encoded


@parameterize_examples
def test_inverse(decoded: bytes, encoded: str):
    assert Base64.inverse(encoded) == decoded


@pytest.mark.parametrize("encoded", ["SGVsbG9", "Qm9uam91ch"])
def test_noncanonical(encoded: str):
    with pytest.raises(BadData) as excinfo:
        Base64.inverse(encoded)
    assert "non-canonical" in str(excinfo.value)
