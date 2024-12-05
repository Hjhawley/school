use super::*;

pub fn parse_clause(tokens: &Vec<Token>) -> Result<Clause, String> {
    let mut parser = Parser::new(tokens);
    let clause = parser.parse_clause()?;
    if parser.current_token().is_some() {
        return Err("Expected to find end of input".to_string());
    }
    Ok(clause)
}

pub fn parse_query(tokens: &Vec<Token>) -> Result<Term, String> {
    let mut parser = Parser::new(tokens);
    let term = parser.parse_term()?;
    parser.expect_token(&Token::Period)?;
    if parser.current_token().is_some() {
        return Err("Expected to find end of input".to_string());
    }
    Ok(term)
}

pub fn tokenize(input: &str) -> Result<Vec<Token>, String> {
    let mut tokens = Vec::new();
    let mut chars = input.chars().peekable();

    while let Some(&ch) = chars.peek() {
        match ch {
            c if c.is_ascii_uppercase() || c == '_' => {
                let mut var_str = String::new();
                while let Some(&ch) = chars.peek() {
                    if ch.is_ascii_alphanumeric() || ch == '_' {
                        var_str.push(ch);
                        chars.next();
                    } else {
                        break;
                    }
                }

                tokens.push(Token::Var(var_str));
            }
            c if c.is_ascii_lowercase() => {
                let mut atom_str = String::new();
                while let Some(&ch) = chars.peek() {
                    if ch.is_ascii_alphanumeric() || ch == '_' {
                        atom_str.push(ch);
                        chars.next();
                    } else {
                        break;
                    }
                }

                tokens.push(Token::Atom(atom_str));
            }
            '(' => {
                tokens.push(Token::LeftParen);
                chars.next();
            }
            ')' => {
                tokens.push(Token::RightParen);
                chars.next();
            }
            '.' => {
                tokens.push(Token::Period);
                chars.next();
            }
            ',' => {
                tokens.push(Token::Comma);
                chars.next();
            }
            ':' => {
                chars.next();
                if let Some(&'-') = chars.peek() {
                    chars.next();
                    tokens.push(Token::ColonHyphen);
                } else {
                    return Err("unexpected character: ':'".to_string());
                }
            }
            c if c.is_whitespace() => {
                chars.next();
            }
            _ => {
                return Err(format!("unexpected character: '{}'", ch));
            }
        }
    }

    Ok(tokens)
}

// grammar:
//
// term             -> variable | atom ( termlist ) | atom
// termlist         -> term | term , termlist
// clause           -> fact | rule
// fact             -> term .
// rule             -> term :- termlist .

struct Parser<'a> {
    tokens: &'a [Token],
    position: usize,
}

impl<'a> Parser<'a> {
    fn new(tokens: &'a [Token]) -> Self {
        Self {
            tokens,
            position: 0,
        }
    }

    fn current_token(&self) -> Option<&Token> {
        self.tokens.get(self.position)
    }

    fn advance(&mut self) {
        self.position += 1;
    }

    fn expect_token(&mut self, expected: &Token) -> Result<(), String> {
        if self.current_token() == Some(expected) {
            self.advance();
            Ok(())
        } else {
            Err(format!(
                "Expected token: {:?}, but found {:?} at position {}",
                expected,
                self.current_token(),
                self.position
            ))
        }
    }

    fn parse_term(&mut self) -> Result<Term, String> {
        match self.current_token() {
            Some(Token::Var(v)) => {
                self.advance();
                Ok(Term::Var(v.clone())) // Clone the string, not the Token
            }
            Some(Token::Atom(a)) => {
                self.advance();
                if let Some(Token::LeftParen) = self.current_token() {
                    self.advance(); // Consume '('
                    let termlist = self.parse_termlist()?;
                    self.expect_token(&Token::RightParen)?; // Consume ')'
                    Ok(Term::Compound {
                        head_atom: a.clone(), // Clone the string, not the Token
                        termlist,
                    })
                } else {
                    Ok(Term::Atom(a.clone())) // Clone the string, not the Token
                }
            }
            _ => Err(format!(
                "Expected a term (variable, atom, or compound term), but found {:?} at position {}",
                self.current_token(),
                self.position
            )),
        }
    }    

    fn parse_termlist(&mut self) -> Result<Vec<Term>, String> {
        let mut terms = Vec::new();
        terms.push(self.parse_term()?);
    
        while matches!(self.current_token(), Some(Token::Comma)) {
            self.advance(); // Consume ','
            terms.push(self.parse_term()?);
        }
    
        Ok(terms)
    }    

    fn parse_fact(&mut self) -> Result<Clause, String> {
        let term = self.parse_term()?;
        self.expect_token(&Token::Period)?; // Consume '.'
        Ok(Clause::Fact(term))
    }

    fn parse_rule(&mut self) -> Result<Clause, String> {
        let head = self.parse_term()?;
        self.expect_token(&Token::ColonHyphen)?; // Consume ':-'
        let termlist = self.parse_termlist()?;
        self.expect_token(&Token::Period)?; // Consume '.'
        Ok(Clause::Rule(head, termlist))
    }

    fn parse_clause(&mut self) -> Result<Clause, String> {
        if self.position + 1 < self.tokens.len()
            && matches!(self.tokens[self.position + 1], Token::ColonHyphen)
        {
            self.parse_rule()
        } else {
            self.parse_fact()
        }
    }

    fn parse_query(&mut self) -> Result<Term, String> {
        let term = self.parse_term()?;
        self.expect_token(&Token::Period)?; // Consume '.'
        Ok(term)
    }
}
