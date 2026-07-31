from wxr_migrate.rewrite import rewrite_media_urls


def test_rewrite_absolute_and_relative_upload_urls():
    html = (
        '<img src="https://panjigautama.com/wp-content/uploads/2021/01/vue-1.png" />'
        '<img src="/wp-content/uploads/2021/01/vue-2.png" />'
    )
    url_map = {
        "https://panjigautama.com/wp-content/uploads/2021/01/vue-1.png": "/images/vue-1.png",
        "https://panjigautama.com/wp-content/uploads/2021/01/vue-2.png": "/images/vue-2.png",
        "/wp-content/uploads/2021/01/vue-1.png": "/images/vue-1.png",
        "/wp-content/uploads/2021/01/vue-2.png": "/images/vue-2.png",
    }
    out = rewrite_media_urls(html, url_map)
    assert "wp-content" not in out
    assert "/images/vue-1.png" in out
    assert "/images/vue-2.png" in out
