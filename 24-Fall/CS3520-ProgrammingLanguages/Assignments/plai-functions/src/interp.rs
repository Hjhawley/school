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
        Exp::Lam { var, body } => {
            // function closure
            Ok(Value::Fun {
                var: var.clone(),
                body: body.clone(),
                nv: nv.clone(),
            })
        },
        Exp::App { fun, arg } => {
            // evaluate function and arg
            let fv = interp(fun, nv)?;
            let av = interp(arg, nv)?;
            match fv {
                Value::Fun { var, body, nv: fun_nv } => {
                    let mut new_env = fun_nv.clone();
                    new_env.insert(var.clone(), av);
                    interp(&body, &new_env)
                },
                _ => Err("didn't get a function".to_string()),
            }
        },
    }
}

fn lookup(s: &str, env: &Env) -> Result<Value, String> {
    if let Some(val) = env.get(s) {
        Ok(val.clone())
    } else {
        Err(format!("{} not bound", s))
    }
}

fn add(v1: Value, v2: Value) -> Result<Value, String> {
    if let (Value::Num(n1), Value::Num(n2)) = (&v1, &v2) {
        Ok(Value::Num(n1 + n2))
    } else {
        Err(format!("+ expects two numbers"))
    }
}

fn boolean_decision(v: Value) -> Result<bool, String> {
    if let Value::Bool(b) = v {
        Ok(b)
    } else {
        Err("boolean expected".to_string())
    }
}
