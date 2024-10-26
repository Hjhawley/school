use super::*;

#[derive(Debug, PartialEq)]
enum Token {
    Number(f64),
    Bool(bool),
    Plus,
    LeftParen,
    RightParen,
    LeftBrace,
    RightBrace,
    If,
    Else,
    Let,
    Equal,
    Symbol(String),
}

pub fn parse_expression(input: &str) -> Result<Exp, String> {
    let tokens = tokenize(input)?;
    println!("tokens: {tokens:?}");
    let mut parser = Parser::new(tokens);
    let exp = parser.parse()?;
    if parser.current_token().is_some() {
        return Err("Expected to find end of input".to_string())
    }
    println!("ast: {exp:#?}");
    Ok(exp)
}

fn tokenize(input: &str) -> Result<Vec<Token>, String> {
    let mut tokens = Vec::new();
    let mut chars = input.chars().peekable();

    while let Some(&ch) = chars.peek() {
        match ch {
            '0'..='9' | '.' | '-' => {
                let mut number_str = String::new();
                number_str.push(ch);
                chars.next();

                while let Some(&ch) = chars.peek() {
                    if ch.is_ascii_digit() || ch == '.' {
                        number_str.push(ch);
                        chars.next();
                    } else {
                        break;
                    }
                }

                match number_str.parse::<f64>() {
                    Ok(number) => tokens.push(Token::Number(number)),
                    Err(_) => return Err(format!("Invalid number format: {}", number_str)),
                }
            }
            '+' => {
                tokens.push(Token::Plus);
                chars.next();
            }
            '(' => {
                tokens.push(Token::LeftParen);
                chars.next();
            }
            ')' => {
                tokens.push(Token::RightParen);
                chars.next();
            }
            '{' => {
                tokens.push(Token::LeftBrace);
                chars.next();
            }
            '}' => {
                tokens.push(Token::RightBrace);
                chars.next();
            }
            '=' => {
                tokens.push(Token::Equal);
                chars.next();
            }
            c if c.is_whitespace() => {
                chars.next();
            }
            c if c.is_ascii_alphabetic() || c == '_' => {
                // Parse identifiers and keywords
                let mut ident_str = String::new();
                while let Some(&ch) = chars.peek() {
                    if ch.is_ascii_alphanumeric() || ch == '_' {
                        ident_str.push(ch);
                        chars.next();
                    } else {
                        break;
                    }
                }

                match ident_str.as_str() {
                    "if" => tokens.push(Token::If),
                    "else" => tokens.push(Token::Else),
                    "true" => tokens.push(Token::Bool(true)),
                    "false" => tokens.push(Token::Bool(false)),
                    "let" => tokens.push(Token::Let),
                    _ => {
                        tokens.push(Token::Symbol(ident_str.clone()));
                    }
                }
            }
            _ => {
                return Err(format!("Unexpected character: '{}'", ch));
            }
        }
    }

    Ok(tokens)
}

struct Parser {
    tokens: Vec<Token>,
    position: usize,
}

// grammar:
// expression       -> term [ + term ]*
// term             -> ( expression ) | conditional | let1 | number | bool | symbol
// conditional      -> if expression { expression } else { expression }
// let1             -> let symbol = expression { expression }

impl Parser {
    fn new(tokens: Vec<Token>) -> Self {
        Parser { tokens, position: 0 }
    }

    fn parse(&mut self) -> Result<Exp, String> {
        self.parse_expression()
    }

    fn parse_expression(&mut self) -> Result<Exp, String> {
        let mut left = self.parse_term()?;

        loop {
            match self.current_token() {
                Some(&Token::Plus) => {
                    self.advance();
                    let right = self.parse_term()?;
                    left = Exp::Plus { left: Box::new(left), right: Box::new(right) };
                },
                _ => {
                    break;
                }
            }
        }

        Ok(left)
    }

    fn parse_term(&mut self) -> Result<Exp, String> {
        match self.current_token() {
            Some(Token::LeftParen) => {
                self.advance();
                let expr = self.parse_expression()?;
                self.expect_token(&Token::RightParen)?;
                Ok(expr)
            },
            Some(Token::If) => self.parse_conditional(),
            Some(Token::Let) => self.parse_let1(),
            Some(&Token::Bool(b)) => {
                self.advance();
                Ok(Exp::Bool(b))
            },
            Some(Token::Number(_)) => self.parse_number(),
            Some(Token::Symbol(_)) => self.parse_symbol(),
            _ => Err(format!("Unexpected token: {:?}", self.current_token())),
        }
    }

    fn parse_conditional(&mut self) -> Result<Exp, String> {
        self.expect_token(&Token::If)?;
        let tst = Box::new(self.parse_expression()?);
        self.expect_token(&Token::LeftBrace)?;
        let thn = Box::new(self.parse_expression()?);
        self.expect_token(&Token::RightBrace)?;
        self.expect_token(&Token::Else)?;
        self.expect_token(&Token::LeftBrace)?;
        let els = Box::new(self.parse_expression()?);
        self.expect_token(&Token::RightBrace)?;
        Ok(Exp::Cnd { tst, thn, els })
    }

    fn parse_let1(&mut self) -> Result<Exp, String> {
        self.expect_token(&Token::Let)?;
        let var = if let Some(Token::Symbol(s)) = self.current_token() {
            let name = s.clone();
            self.advance();
            name
        } else {
            return Err("Expected a symbol after 'let'".to_string());
        };
        self.expect_token(&Token::Equal)?;
        let value = Box::new(self.parse_expression()?);
        self.expect_token(&Token::LeftBrace)?;
        let body = Box::new(self.parse_expression()?);
        self.expect_token(&Token::RightBrace)?;
        Ok(Exp::Let1 { var, value, body })
    }

    fn parse_number(&mut self) -> Result<Exp, String> {
        if let Some(Token::Number(value)) = self.current_token() {
            let number_exp = Exp::Num(*value);
            self.advance();
            Ok(number_exp)
        } else {
            Err("Expected a number".to_string())
        }
    }

    fn parse_symbol(&mut self) -> Result<Exp, String> {
        if let Some(Token::Symbol(s)) = self.current_token() {
            let name = s.clone();
            self.advance();
            Ok(Exp::Var(name))
        } else {
            Err("Expected a symbol".to_string())
        }
    }

    fn expect_token(&mut self, expected: &Token) -> Result<(), String> {
        if self.current_token() == Some(expected) {
            self.advance();
            Ok(())
        } else {
            Err(format!("Expected '{:?}' token", expected))
        }
    }

    fn current_token(&self) -> Option<&Token> {
        self.tokens.get(self.position)
    }

    fn advance(&mut self) {
        self.position += 1;
    }
}
