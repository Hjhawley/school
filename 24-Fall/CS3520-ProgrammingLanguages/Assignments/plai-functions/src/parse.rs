use super::*;

#[derive(Debug, PartialEq)]
enum Token {
    Number(f64),
    Bool(bool),
    Symbol(String),
    Plus,
    LeftParen,
    RightParen,
    LeftBrace,
    RightBrace,
    Equal,
    If,
    Else,
    Let,
    Fn,
}

pub fn parse_expression(input: &str) -> Result<Exp, String> {
    let tokens = tokenize(input)?;
    println!("tokens: {tokens:?}");
    let mut parser = Parser::new(tokens);
    let exp = parser.parse()?;
    if parser.current_token().is_some() {
        return Err("Expected to find end of input".to_string());
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

                // Match keywords or push as identifier
                match ident_str.as_str() {
                    "if" => tokens.push(Token::If),
                    "else" => tokens.push(Token::Else),
                    "let" => tokens.push(Token::Let),
                    "true" => tokens.push(Token::Bool(true)),
                    "false" => tokens.push(Token::Bool(false)),
                    "fn" => tokens.push(Token::Fn),
                    _ => tokens.push(Token::Symbol(ident_str)),
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
// term             -> factor [ ( expression ) ]*
// factor           -> ( expression ) | conditional | let1 | lambda | number | bool | symbol
// conditional      -> if expression { expression } else { expression }
// let1             -> let symbol = expression { expression }
// lambda           -> fn ( symbol ) { expression }

impl Parser {
    fn new(tokens: Vec<Token>) -> Self {
        Parser { tokens, position: 0 }
    }

    fn parse(&mut self) -> Result<Exp, String> {
        self.parse_expression()
    }

    fn parse_expression(&mut self) -> Result<Exp, String> {
        let mut left = self.parse_term()?;

        while let Some(&Token::Plus) = self.current_token() {
            self.expect_token(&Token::Plus)?;
            let right = self.parse_term()?;
            left = Exp::Plus {
                left: Box::new(left),
                right: Box::new(right),
            };
        }

        Ok(left)
    }

    fn parse_term(&mut self) -> Result<Exp, String> {
        let mut term = self.parse_factor()?;

        while let Some(&Token::LeftParen) = self.current_token() {
            let fun = Box::new(term);
            self.expect_token(&Token::LeftParen)?;
            let arg = Box::new(self.parse_expression()?);
            self.expect_token(&Token::RightParen)?;
            term = Exp::App { fun, arg };
        }

        Ok(term)
    }

    fn parse_factor(&mut self) -> Result<Exp, String> {
        match self.current_token() {
            Some(Token::LeftParen) => {
                // ( expr )
                self.expect_token(&Token::LeftParen)?;
                let expr = self.parse_expression()?;
                self.expect_token(&Token::RightParen)?;
                Ok(expr)
            }

            Some(Token::If) => self.parse_conditional(),

            Some(Token::Let) => self.parse_let1(),

            Some(Token::Fn) => self.parse_lambda(),

            Some(&Token::Bool(b)) => {
                self.advance();
                Ok(Exp::Bool(b))
            }

            Some(Token::Symbol(s)) => {
                let name = s.clone();
                self.advance();
                Ok(Exp::Var(name))
            }

            Some(&Token::Number(n)) => {
                self.advance();
                Ok(Exp::Num(n))
            }

            _ => Err("Expected a factor".to_string()),
        }
    }

    fn parse_conditional(&mut self) -> Result<Exp, String> {
        // if cnd { thn } else { els }
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
        // let symbol = exp { exp }
        self.expect_token(&Token::Let)?;
        let Some(Token::Symbol(s)) = self.current_token() else {
            return Err("Expected an indentifier".to_string());
        };
        let var = s.clone();
        self.advance();
        self.expect_token(&Token::Equal)?;
        let value = Box::new(self.parse_expression()?);
        self.expect_token(&Token::LeftBrace)?;
        let body = Box::new(self.parse_expression()?);
        self.expect_token(&Token::RightBrace)?;
        Ok(Exp::Let1 { var, value, body })
    }

    fn parse_lambda(&mut self) -> Result<Exp, String> {
        // fn ( symbol ) { exp }
        self.expect_token(&Token::Fn)?;
        self.expect_token(&Token::LeftParen)?;
        let Some(Token::Symbol(s)) = self.current_token() else {
            return Err("Expected an indentifier".to_string());
        };
        let var = s.clone();
        self.advance();
        self.expect_token(&Token::RightParen)?;
        self.expect_token(&Token::LeftBrace)?;
        let body = Box::new(self.parse_expression()?);
        self.expect_token(&Token::RightBrace)?;
        Ok(Exp::Lam { var, body })
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
