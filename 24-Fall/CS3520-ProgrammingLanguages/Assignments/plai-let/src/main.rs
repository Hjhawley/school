mod parse;
mod interp;

use parse::parse_expression;
use interp::interp;
use std::collections::HashMap;
use std::io;

#[derive(Debug, PartialEq)]
enum Exp {
    Num(f64),
    Bool(bool),
    Var(String),
    Plus { left: Box<Exp>, right: Box<Exp> },
    Cnd { tst: Box<Exp>, thn: Box<Exp>, els: Box<Exp> },
    Let1 { var: String, value: Box<Exp>, body: Box<Exp> },
}

#[derive(Debug, PartialEq, Clone)]
enum Value {
    Num(f64),
    Bool(bool),
}

type Env = HashMap<String, Value>;

fn main() {
    let empty_env = HashMap::new();

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
                match interp(&ast, &empty_env) {
                    Ok(Value::Num(n)) => println!("{n}"),
                    Ok(Value::Bool(b)) => println!("{b}"),
                    Err(msg) => println!("Runtime error: {msg}"),
                }
            }
            Err(error) => println!("Parse error: {}", error),
        }
    }
}
