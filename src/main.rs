use image::{ImageBuffer, Pixel, Rgb, RgbImage};
use scarlet::{color::RGBColor, colormap::ColorMap, colormap::GradientColorMap};

fn main() {
    //Defining Image ratio, resolution, range etc.
    let height: u32 = 2160;
    let image_ratio: f32 = 16.0 / 9.0;
    let width: u32 = ((height as f32) * (image_ratio)) as u32;
    let range_x: [f32; 2] = [(-1.5 * image_ratio), (3.0 * image_ratio)];
    let x_unit: f32 = range_x[1] / width as f32;
    let range_y: [f32; 2] = [-1.5, 3.0];
    let y_unit: f32 = range_y[1] / height as f32;
    //Set c in the formula z = z**2 + c
    let julia_cmplx: (f32, f32) = (-0.4, 0.6);
    //Setting up ImgBuffer with 2 gradientmaps, since only 2 colors per map are allowed
    let mut img: RgbImage = ImageBuffer::new(width, height);
    let grad_color_1 = RGBColor::from_hex_code("#1a1a24").unwrap();
    let grad_color_2 = RGBColor::from_hex_code("#b0afba").unwrap();
    let grad_color_3 = RGBColor::from_hex_code("#00f2ff").unwrap();
    let cmap1 = GradientColorMap::new_linear(grad_color_1, grad_color_2);
    let cmap2 = GradientColorMap::new_linear(grad_color_2, grad_color_3);

    for x in 0..width {
        for y in 0..height {
            let mut zx = range_x[0] + x as f32 * (x_unit);
            let mut zy = range_y[0].abs() - y as f32 * (y_unit);
            let mut iterator: u32 = 0;

            while (zx * zx + zy * zy) <= 4.0 && iterator < 255 {
                let xtemp = zx * zx - (zy * zy);
                zy = (2.0 * zx * zy) + julia_cmplx.1;
                zx = xtemp + julia_cmplx.0;
                iterator += 1;
            }

            let it_col: RGBColor;
            if iterator <= 128 {
                it_col = cmap1.transform_single((1.0 / 128.0) * iterator as f64)
            } else {
                it_col = cmap2.transform_single((1.0 / 128.0) * (iterator - 128) as f64)
            }
            let pixel = Rgb::from_channels(
                (it_col.r * 255.0) as u8,
                (it_col.g * 255.0) as u8,
                (it_col.b * 255.0) as u8,
                0,
            );
            img.put_pixel(x, y, pixel);
        }
        if x % 100 == 0 {
            println!("Row {} / {} completed.", x, width);
        }
    }

    let _ = img.save("julia.png");
}
