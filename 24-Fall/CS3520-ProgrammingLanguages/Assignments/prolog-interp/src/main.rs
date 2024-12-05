mod parse;

use parse::parse_clause;
use parse::parse_query;
use parse::tokenize;
use std::fmt;
use std::io;

#[derive(Debug, PartialEq)]
enum Token {
    Var(String),
    Atom(String),
    LeftParen,
    RightParen,
    Period,
    Comma,
    ColonHyphen,
}

impl fmt::Display for Token {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Token::Var(v) => write!(f, "{v}"),
            Token::Atom(a) => write!(f, "{a}"),
            Token::LeftParen => write!(f, "("),
            Token::RightParen => write!(f, ")"),
            Token::Period => write!(f, "."),
            Token::Comma => write!(f, ","),
            Token::ColonHyphen => write!(f, ":-"),
        }
    }
}

#[derive(Debug, PartialEq, Clone)]
enum Term {
    Var(String),
    Atom(String),
    Compound { head_atom: String, termlist: Vec<Term> },
}

impl fmt::Display for Term {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Term::Var(v) => write!(f, "{v}"),
            Term::Atom(a) => write!(f, "{a}"),
            Term::Compound { head_atom, termlist } => {
                write!(f, "{head_atom}(")?;
                let mut sep = "";
                for t in termlist {
                    write!(f, "{sep}{t}")?;
                    sep = ",";
                }
                write!(f, ")")
            }
        }
    }
}

enum Clause {
    Fact(Term),
    Rule(Term, Vec<Term>),
}

impl fmt::Display for Clause {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            Clause::Fact(t) => {
                write!(f, "{t}")?;
            }
            Clause::Rule(head, lst) => {
                write!(f, "{head} :- ")?;
                let mut sep = "";
                for elt in lst {
                    write!(f, "{sep}{elt}")?;
                    sep = ", ";
                }
            }
        }
        writeln!(f, ".")
    }
}

fn main() {
    // print a prompt
    println!("\nPlease enter clauses (blank line to end the database):");

    let mut program = Vec::new();
    loop {
        // get one clause
        let mut tokens = Vec::new();
        loop {
            // read a line of input, quit on ctrl-d and skip empty lines
            let mut input = String::new();
            let len = io::stdin()
                .read_line(&mut input)
                .expect("Failed to read line");
            if len == 0 {
                return;
            }
            if input.trim().is_empty() {
                break;
            }

            // tokenize
            match tokenize(input.trim()) {
                Ok(new_tokens) => {
                    tokens.extend(new_tokens);
                }
                Err(msg) => {
                    println!("Tokenizer error: {msg}");
                    return;
                }
            };

            // finish if the last token was a period
            if let Some(Token::Period) = tokens.last() {
                break;
            }
        }
        if tokens.is_empty() {
            break;
        }

        print!("tokens: [");
        let mut sep = "";
        for t in &tokens {
            print!("{sep}{t}");
            sep = " ";
        }
        println!("]");

        // parse
        let clause = match parse_clause(&tokens) {
            Ok(clause) => clause,
            Err(msg) => {
                println!("Parse error: {msg}");
                return;
            }
        };
        println!("clause: {clause}");
        program.push(clause);
    }

    loop {
        // get one query
        println!("Please enter a query (blank line to quit):");
        let mut tokens = Vec::new();
        loop {
            // read a line of input, quit on ctrl-d and skip empty lines
            let mut input = String::new();
            let len = io::stdin()
                .read_line(&mut input)
                .expect("Failed to read line");
            if len == 0 {
                return;
            }
            if input.trim().is_empty() {
                break;
            }

            // tokenize
            match tokenize(input.trim()) {
                Ok(new_tokens) => {
                    tokens.extend(new_tokens);
                }
                Err(msg) => {
                    println!("Tokenizer error: {msg}");
                    return;
                }
            };

            // finish if the last token was a period
            if let Some(Token::Period) = tokens.last() {
                break;
            }
        }
        if tokens.is_empty() {
            break;
        }

        print!("tokens: [");
        let mut sep = "";
        for t in &tokens {
            print!("{sep}{t}");
            sep = " ";
        }
        println!("]");

        // parse
        let query = match parse_query(&tokens) {
            Ok(term) => term,
            Err(msg) => {
                println!("Parse error: {msg}");
                return;
            }
        };
        println!("query: {query}.");
    }
}
