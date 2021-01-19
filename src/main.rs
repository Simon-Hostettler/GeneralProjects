use image::{ImageBuffer, Pixel, Rgb, RgbImage};
use num::Complex;
use scarlet::{color::RGBColor, colormap::ColorMap, colormap::GradientColorMap};

fn main() {
    let height: u32 = 1080;
    let image_ratio: f32 = 16.0 / 9.0;
    let width: u32 = ((height as f32) * (image_ratio)) as u32;
    let range_x: [f32; 2] = [(-1.5 * image_ratio), (3.0 * image_ratio)];
    let range_y: [f32; 2] = [-1.5, 3.0];
    let jcmplx: (f32, f32) = (-0.4, 0.6);
    let mut img: RgbImage = ImageBuffer::new(width, height);
    let col1 = RGBColor::from_hex_code("#1a1a24").unwrap();
    let col2 = RGBColor::from_hex_code("#00f2ff").unwrap();
    let cmap = GradientColorMap::new_linear(col1, col2);

    for x in 0..width {
        for y in 0..height {
            let iter: f64 = julia_it(
                (
                    range_x[0] + x as f32 * (range_x[1] / width as f32),
                    range_y[0].abs() - y as f32 * (range_y[1] / height as f32),
                ),
                jcmplx,
            );
            let it_col = cmap.transform_single((1.0 / 255.0) * iter);
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

pub fn julia_it((compx, compy): (f32, f32), (jcompx, jcompy): (f32, f32)) -> f64 {
    let mut value = Complex::new(compx, compy);
    let jul_cmplx = Complex::new(jcompx, jcompy);
    let mut iterator: f64 = 0.0;
    while value.norm() <= 4.0 && iterator < 255.0 {
        value = (value.powf(2.0)) + jul_cmplx;
        iterator += 1.0;
    }
    iterator
}
