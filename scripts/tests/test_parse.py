from pathlib import Path
from wxr_migrate.parse import parse_wxr

FIXTURE = Path(__file__).parent / "fixtures" / "mini-posts.xml"


def test_parse_wxr_reads_published_and_draft():
    items = parse_wxr(FIXTURE)
    assert len(items) == 2
    published = [i for i in items if i.status == "publish"]
    assert len(published) == 1
    post = published[0]
    assert post.title == "Hello World"
    assert post.slug == "hello-world"
    assert post.post_type == "post"
    assert post.categories == ["Management"]
    assert post.tags == ["notes"]
    assert "vue-1.png" in post.content_html
