extern crate libc;


use std::convert::From;

use std::error::Error;
use std::fs::File;
use std::io;
use std::ptr;

use regex::Regex;

use util::{Context, cstr_to_str, to_raw_ptr};


#[no_mangle]
pub extern "C" fn regex_new(ctx: *mut Context, c_pat: *mut libc::c_char) -> *mut Regex {
    let pat = cstr_to_str(c_pat);
    let re = with_context!(ctx, ptr::null_mut(), Regex::new(pat));
    to_raw_ptr(re)
}

make_free_fn!(regex_free, *mut Regex);

//#[no_mangle]
//pub extern "C" fn regex_with_size_limit(ctx: *mut Context, c_siz: *mut libc::size_t, c_pat: *mut libc::c_char) -> *mut Regex {
//    let size = c_siz as usize;
//    let pat = cstr_to_str(c_pat);
//    let re = with_context!(ctx, ptr::null_mut(), Regex::with_size_limit(size, pat));
//    to_raw_ptr(re)
//}

#[no_mangle]
pub extern "C" fn regex_is_match(ptr: *mut Regex, s: *mut libc::c_char) -> bool {
    let regex = mutref_from_ptr!(ptr);
    regex.is_match(cstr_to_str(s))
}

// A struct that can be passed between C and Rust
#[repr(C)]
pub struct FindResult {
    start: libc::int32_t,
    end: libc::int32_t,
}


// Conversion functions
impl From<(i32, i32)> for FindResult {
    fn from(tup: (i32, i32)) -> FindResult {
        FindResult { start: tup.0, end: tup.1}
    }
}

#[no_mangle]
//pub extern "C" fn regex_find(ptr: *mut Regex, s: *mut libc::c_char) -> [libc::int32_t; 2] {
pub extern "C" fn regex_find(ptr: *mut Regex, s: *mut libc::c_char) -> FindResult {
    let regex = mutref_from_ptr!(ptr);
    match regex.find(cstr_to_str(s)) {
        None => {
            (-1, -1).into()
        },
        Some((match_start, match_end)) => {
            (match_start as i32, match_end as i32).into()
        },
    }

}
make_free_fn!(regex_findresult_free, *mut FindResult);
