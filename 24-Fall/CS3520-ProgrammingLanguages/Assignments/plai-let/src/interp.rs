use super::*;

pub fn interp(e: &Exp, nv: &Env) -> Result<Value, String> {
    match e {
        Exp::Num(n) => Ok(Value::Num(*n)),
        Exp::Bool(b) => Ok(Value::Bool(*b)),
        Exp::Var(s) => lookup(s, nv),
        Exp::Plus { left, right } =>
            add(interp(left, nv)?, interp(right, nv)?),
        Exp::Cnd { tst, thn, els } =>
            if boolean_decision(interp(tst, nv)?)? {
                interp(thn, nv)
            } else {
                interp(els, nv)
            },
        Exp::Let1 { var, value, body } => {
            let val = interp(value, nv)?;
            let mut new_env = nv.clone();
            new_env.insert(var.clone(), val);
            interp(body, &new_env)
        },
    }
}

fn lookup(s: &str, env: &Env) -> Result<Value, String> {
    if let Some(val) = env.get(s) {
        Ok(val.clone())
    } else {
        Err(format!("Variable '{}' not found", s))
    }
}

fn add(v1: Value, v2: Value) -> Result<Value, String> {
    if let (Value::Num(n1), Value::Num(n2)) = (&v1, &v2) {
        Ok(Value::Num(n1 + n2))
    } else {
        Err(format!("+ expects two numbers, got {:?} + {:?}", v1, v2))
    }
}

fn boolean_decision(v: Value) -> Result<bool, String> {
    if let Value::Bool(b) = v {
        Ok(b)
    } else {
        Err(format!("boolean expected, found {:?}", v))
    }
}
