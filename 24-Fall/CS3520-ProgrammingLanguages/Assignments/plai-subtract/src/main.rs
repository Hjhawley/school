mod parse;
mod calc;

use parse::parse_expression;
use calc::calc;
use std::io;

#[derive(Debug, PartialEq)]
enum Exp {
    Num(f64),
    Bool(bool),
    Plus { left: Box<Exp>, right: Box<Exp> },
    Minus { left: Box<Exp>, right: Box<Exp> },
    Cnd { tst: Box<Exp>, thn: Box<Exp>, els: Box<Exp> },
}

#[derive(Debug, PartialEq)]
enum Value {
    Num(f64),
    Bool(bool),
}

fn main() {
    loop {
        // print a prompt
        println!("\nPlease enter an expression:");

        // read a line of input, quit on ctrl-d and skip empty lines
        let mut input = String::new();
        let len = io::stdin().read_line(&mut input)
            .expect("Failed to read line");
        if len == 0 { break; }
        if input.trim().is_empty() { continue; }

        // parse and evaluate
        match parse_expression(input.trim()) {
            Ok(ast) => {
                match calc(&ast) {
                    Ok(Value::Num(n)) => println!("{n}"),
                    Ok(Value::Bool(b)) => println!("{b}"),
                    Err(msg) => println!("Runtime error: {msg}"),
                }
            }
            Err(error) => println!("Parse error: {}", error),
        }
    }
}
