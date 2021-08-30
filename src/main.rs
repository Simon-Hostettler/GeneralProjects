extern crate image;
use image::{ImageBuffer, Pixel, Rgb};
use std::path::Path;
use std::string::String;

fn main() {
    encode(Path::new(""), "Nobody expects the spanish inquisition");
    let msg = decode(Path::new(""));
    println!("{}", msg);
}

fn encode(source: &Path, msg: &str) {
    //convert message to bytearray which will be stored
    let msg_bytes: &[u8] = msg.as_bytes();
    let msg_length = msg_bytes.len();

    //load image to encode
    let mut image: ImageBuffer<Rgb<u8>, Vec<u8>> = image::open(source).unwrap().to_rgb8();
    let (w, h) = (image.width(), image.height());
    let mut pixel_counter = 0;
    if (msg_length * 4) as u32 > w * h {
        panic!("Not enough pixels to store message")
    };
    //encode number of characters to be written, will be stored in first 16 pixels
    for i in (0..=15).rev() {
        let cur_pixel = get_pixel_pos(pixel_counter, w);
        let oc_pixel = image.get_pixel(cur_pixel.0, cur_pixel.1);
        let (r, g, mut b) = (oc_pixel[0], oc_pixel[1], oc_pixel[2]);
        b = (b & 0b11111100) | (((msg_length >> i * 2) as u8) & 0b00000011);
        let new_pixel = Rgb::from_channels(r, g, b, 0);
        image.put_pixel(cur_pixel.0, cur_pixel.1, new_pixel);
        pixel_counter += 1;
    }
    //encode message in the LSB of the blue channel of pixels, 2 bits per pixel
    for character in msg_bytes {
        let char_parts = [
            (character & 0b11000000) >> 6,
            (character & 0b00110000) >> 4,
            (character & 0b00001100) >> 2,
            character & 0b00000011,
        ];
        for i in 0..=3 {
            let cur_pixel = get_pixel_pos(pixel_counter, w);
            let oc_pixel = image.get_pixel(cur_pixel.0, cur_pixel.1);
            let (r, g, mut b) = (oc_pixel[0], oc_pixel[1], oc_pixel[2]);
            b = (b & 0b11111100) | char_parts[i];
            let new_pixel = Rgb::from_channels(r, g, b, 0);
            image.put_pixel(cur_pixel.0, cur_pixel.1, new_pixel);
            pixel_counter += 1;
        }
    }
    let _ = image.save("pictures/encoded_image.png");
    println!("Successfully encoded image");
}
fn decode(source: &Path) -> String {
    let image: ImageBuffer<Rgb<u8>, Vec<u8>> = image::open(source).unwrap().to_rgb8();
    let w = image.width();
    let mut msg_length: u32 = 0;
    let mut pixel_counter = 0;
    //read number of encoded characters from the first 16 bits
    for i in (0..=15).rev() {
        let cur_pixel = get_pixel_pos(pixel_counter, w);
        let oc_pixel = image.get_pixel(cur_pixel.0, cur_pixel.1);
        let b = oc_pixel[2];
        msg_length |= ((b & 0b00000011) as u32) << i * 2;
        pixel_counter += 1;
    }
    let mut msg_bytes: Vec<u8> = Vec::new();
    //read encoded characters, 2 bits per pixel (stored in LSB of blue channel)
    for _ in 0..msg_length {
        let mut character: u8 = 0;
        for j in (0..=3).rev() {
            let cur_pixel = get_pixel_pos(pixel_counter, w);
            let oc_pixel = image.get_pixel(cur_pixel.0, cur_pixel.1);
            let b = oc_pixel[2];
            character |= (b & 0b00000011) << j * 2;
            pixel_counter += 1;
        }
        msg_bytes.push(character);
    }
    let res = std::str::from_utf8(&msg_bytes[..]);
    match res {
        Ok(msg) => msg.to_string(),
        Err(e) => {
            println!("Error: {}", e);
            "".to_string()
        }
    }
}

fn get_pixel_pos(counter: u32, w: u32) -> (u32, u32) {
    (counter % w, counter / w)
}
