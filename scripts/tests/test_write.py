from pathlib import Path
from wxr_migrate.parse import ContentItem
from wxr_migrate.write import write_content


def test_write_content_posts_and_pages(tmp_path: Path):
    items = [
        ContentItem(
            title="Hello",
            slug="hello",
            date="2021-01-15 10:00:00",
            lastmod="2021-01-16 11:00:00",
            status="publish",
            post_type="post",
            categories=["Management"],
            tags=[],
            content_html='<p>Hi <img src="https://panjigautama.com/wp-content/uploads/2021/01/vue-1.png" /></p>',
        ),
        ContentItem(
            title="About Me",
            slug="about-me",
            date="2021-01-01 10:00:00",
            lastmod="2021-01-01 10:00:00",
            status="publish",
            post_type="page",
            categories=[],
            tags=[],
            content_html="<p>About</p>",
        ),
        ContentItem(
            title="Draft",
            slug="draft",
            date="2021-01-01 10:00:00",
            lastmod="2021-01-01 10:00:00",
            status="draft",
            post_type="post",
            categories=[],
            tags=[],
            content_html="<p>x</p>",
        ),
    ]
    url_map = {
        "https://panjigautama.com/wp-content/uploads/2021/01/vue-1.png": "/images/vue-1.png",
        "/wp-content/uploads/2021/01/vue-1.png": "/images/vue-1.png",
    }
    posts, pages = write_content(items, url_map, tmp_path)
    assert posts == 1
    assert pages == 1
    post = (tmp_path / "blog" / "hello.md").read_text()
    assert 'title: "Hello"' in post
    assert "categories:" in post
    assert "/images/vue-1.png" in post
    assert "wp-content" not in post
    assert (tmp_path / "about-me.md").exists()
