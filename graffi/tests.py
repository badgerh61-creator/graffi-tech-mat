from pathlib import Path
def generate_tests():
    p = Path('tests/graffi_helper')
    p.mkdir(parents=True, exist_ok=True)
    (p / 'test_model_generation.py').write_text("""from pathlib import Path

def test_model_exists():
    assert Path('.graffi_helper_model/semantic_model.json').exists()
""")
    return p
