from pathlib import Path
from wxr_migrate.media import choose_filename


def test_choose_filename_avoids_collision(tmp_path: Path):
    (tmp_path / "vue-1.png").write_bytes(b"a")
    name = choose_filename(
        source_url="https://panjigautama.com/wp-content/uploads/2022/01/vue-1.png",
        images_dir=tmp_path,
        reserved={"vue-1.png": "https://other/vue-1.png"},
    )
    assert name != "vue-1.png"
    assert name.endswith(".png")
