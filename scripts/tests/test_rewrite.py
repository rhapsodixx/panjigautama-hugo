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


def test_rewrite_wordpress_size_variant_urls():
    html = (
        '<img src="https://panjigautama.com/wp-content/uploads/2021/01/vue-4-843x1024.jpeg" />'
        '<img src="/wp-content/uploads/2021/01/photo-1024x399.png" />'
        '<a href="https://panjigautama.com/wp-content/uploads/2021/01/vue-4.jpeg">full</a>'
    )
    url_map = {
        "https://panjigautama.com/wp-content/uploads/2021/01/vue-4.jpeg": "/images/vue-4.jpeg",
        "/wp-content/uploads/2021/01/vue-4.jpeg": "/images/vue-4.jpeg",
        "https://panjigautama.com/wp-content/uploads/2021/01/photo.png": "/images/photo.png",
        "/wp-content/uploads/2021/01/photo.png": "/images/photo.png",
    }
    out = rewrite_media_urls(html, url_map)
    assert "wp-content" not in out
    assert "843x1024" not in out
    assert "1024x399" not in out
    assert out.count("/images/vue-4.jpeg") == 2
    assert "/images/photo.png" in out


def test_rewrite_size_variant_falls_back_to_scaled_attachment():
    html = (
        '<img src="https://panjigautama.com/wp-content/uploads/2025/09/IMG_2675-768x1024.jpg" />'
    )
    url_map = {
        "https://panjigautama.com/wp-content/uploads/2025/09/IMG_2675-scaled.jpg": (
            "/images/IMG_2675-scaled.jpg"
        ),
        "/wp-content/uploads/2025/09/IMG_2675-scaled.jpg": "/images/IMG_2675-scaled.jpg",
    }
    out = rewrite_media_urls(html, url_map)
    assert "wp-content" not in out
    assert "/images/IMG_2675-scaled.jpg" in out
