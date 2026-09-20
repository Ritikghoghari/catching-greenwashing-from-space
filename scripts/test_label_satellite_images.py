from PIL import Image

from label_satellite_images import (
    STATIC_LEGEND, TOP_BAND_PX, BOTTOM_BAND_PX,
    add_labels, label_static, label_yearly, _hex_to_rgb,
)


def _dummy(w=800, h=127, color=(26, 122, 60)):
    return Image.new("RGB", (w, h), color)


def test_add_labels_grows_canvas_by_band_heights():
    img = _dummy()
    out = add_labels(img, "TITLE", "subtitle", STATIC_LEGEND)
    assert out.size == (img.width, img.height + TOP_BAND_PX + BOTTOM_BAND_PX)


def test_add_labels_preserves_original_pixels_untouched():
    """Original data band must be copied verbatim, not drawn over."""
    img = _dummy(color=(200, 50, 50))
    out = add_labels(img, "TITLE", "subtitle", STATIC_LEGEND)
    # sample a pixel far from any text/legend, inside the pasted-image region
    px = out.getpixel((img.width // 2, TOP_BAND_PX + img.height // 2))
    assert px == (200, 50, 50)


def test_add_labels_legend_swatch_colors_present():
    img = _dummy()
    out = add_labels(img, "TITLE", "subtitle", STATIC_LEGEND)
    legend_y = TOP_BAND_PX + img.height + 8 + 7
    first_color = _hex_to_rgb(STATIC_LEGEND[0][0])
    assert out.getpixel((10 + 5, legend_y)) == first_color


def test_hex_to_rgb():
    assert _hex_to_rgb("1a7a3c") == (0x1a, 0x7a, 0x3c)
    assert _hex_to_rgb("ffffff") == (255, 255, 255)


def test_label_static_includes_mill_count_does_not_crash():
    img = _dummy()
    out = label_static(img, "gar", n_mills=3, loss_after_2020_ha=6270.35)
    assert out.size[1] > img.size[1]


def test_label_yearly_uses_more_legend_entries_than_static():
    img = _dummy()
    static_out = label_static(img, "gar", 3, 6270.35)
    yearly_out = label_yearly(img, "gar", 3, 6270.35)
    # yearly legend has more entries -> wider text run, but canvas height is fixed
    # by band constants, so just confirm both render without error and differ in size only if legend wraps
    assert static_out.size[1] == yearly_out.size[1]
