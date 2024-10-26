use super::*;

pub fn calc(e: &Exp) -> Result<Value, String> {
    match e {
        Exp::Num(n) => Ok(Value::Num(*n)),
        Exp::Bool(b) => Ok(Value::Bool(*b)),
        Exp::Plus { left, right } => add(calc(left)?, calc(right)?),
        Exp::Minus { left, right } => subtract(calc(left)?, calc(right)?),
        Exp::Cnd { tst, thn, els } => {
            if boolean_decision(calc(tst)?)? {
                calc(thn)
            } else {
                calc(els)
            }
        }
    }
}

fn add(v1: Value, v2: Value) -> Result<Value, String> {
    if let (Value::Num(n1), Value::Num(n2)) = (&v1, &v2) {
        Ok(Value::Num(n1 + n2))
    } else {
        Err(format!("+ expects two numbers, got {:?} + {:?}", v1, v2))
    }
}

fn subtract(v1: Value, v2: Value) -> Result<Value, String> {
    if let (Value::Num(n1), Value::Num(n2)) = (&v1, &v2) {
        Ok(Value::Num(n1 - n2))
    } else {
        Err(format!("- expects two numbers, got {:?} - {:?}", v1, v2))
    }
}

fn boolean_decision(v: Value) -> Result<bool, String> {
    if let Value::Bool(b) = &v {
        Ok(*b)
    } else {
        Err(format!("boolean expected, found {:?}", v))
    }
}
