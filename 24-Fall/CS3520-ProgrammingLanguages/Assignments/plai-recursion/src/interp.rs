use super::*;
use std::rc::Rc;
use std::cell::RefCell;

type Env = HashMap<String, Rc<RefCell<Option<Value>>>>; // need to allow variables to refer to themselves during their own definition

pub fn tc(e: &Exp, tnv: &TEnv) -> Result<Type, String> {
    match e {
        Exp::Int(_) => Ok(Type::Int),
        Exp::Bool(_) => Ok(Type::Bool),
        Exp::Str(_) => Ok(Type::Str),
        Exp::Var(var) => lookup_type(var, tnv),
        Exp::Plus { left, right } => {
            let left_type = tc(left, tnv)?;
            let right_type = tc(right, tnv)?;
            if left_type == Type::Int && right_type == Type::Int {
                Ok(Type::Int)
            } else {
                Err("not both integers".to_string())
            }
        },
        Exp::LessThan { left, right } => {
            let left_type = tc(left, tnv)?;
            let right_type = tc(right, tnv)?;
            if left_type == Type::Int && right_type == Type::Int {
                Ok(Type::Bool)
            } else {
                Err("not both numbers".to_string())
            }
        },
        Exp::Concat { left, right } => {
            let left_type = tc(left, tnv)?;
            let right_type = tc(right, tnv)?;
            if left_type == Type::Str && right_type == Type::Str {
                Ok(Type::Str)
            } else {
                Err("not both strings".to_string())
            }
        },
        Exp::Cnd { tst, thn, els } => {
            let tst_type = tc(tst, tnv)?;
            if tst_type != Type::Bool {
                return Err("condition must be a bool".to_string());
            }
            let thn_type = tc(thn, tnv)?;
            let els_type = tc(els, tnv)?;
            if thn_type == els_type {
                Ok(thn_type)
            } else {
                Err("then and else branches have different types".to_string())
            }
        },
        Exp::Let1 { var, value, body } => {
            let val_type = tc(value, tnv)?;
            let mut new_tnv = tnv.clone();
            new_tnv.insert(var.clone(), val_type);
            tc(body, &new_tnv)
        },
        Exp::Rec { var, var_type, value, body } => {
            // Insert the variable with its declared type into the type environment
            let mut new_tnv = tnv.clone();
            new_tnv.insert(var.clone(), var_type.clone());
            // Type check the value in the new environment
            let val_type = tc(value, &new_tnv)?;
            // make sure the declared type matches the type of the value
            if val_type != var_type.clone() {
                Err(format!(
                    "Type mismatch in recursive definition of {}: expected {}, got {}",
                    var, var_type, val_type
                ))
            } else {
                // Type check the body in the new environment
                tc(body, &new_tnv)
            }
        },
        Exp::Lam { var, var_type, body } => {
            let mut new_tnv = tnv.clone();
            new_tnv.insert(var.clone(), var_type.clone());
            let body_type = tc(body, &new_tnv)?;
            Ok(Type::Fun {
                param: Box::new(var_type.clone()),
                result: Box::new(body_type),
            })
        },
        Exp::App { fun, arg } => {
            let fun_type = tc(fun, tnv)?;
            let arg_type = tc(arg, tnv)?;
            match fun_type {
                Type::Fun { param, result } => {
                    if *param == arg_type {
                        Ok(*result)
                    } else {
                        Err(format!(
                            "Function expected argument of type {}, but got {}",
                            param, arg_type
                        ))
                    }
                },
                _ => Err("Attempted to call a non-function".to_string()),
            }
        },
    }
}

fn lookup_type(var: &str, tnv: &TEnv) -> Result<Type, String> {
    if let Some(t) = tnv.get(var) {
        Ok(t.clone())
    } else {
        Err(format!("no known type for {}", var))
    }
}

pub fn interp(e: &Exp, nv: &Env) -> Result<Value, String> {
    match e {

        Exp::Int(n) => Ok(Value::Int(*n)),
        Exp::Str(s) => Ok(Value::Str(s.clone())),
        Exp::Bool(b) => Ok(Value::Bool(*b)),
        Exp::Var(s) => lookup(s, nv),

        Exp::Plus { left, right } => {
            let v1 = interp(left, nv)?;
            let v2 = interp(right, nv)?;
            add(&v1, &v2)
        }
        Exp::Concat { left, right } => {
            let v1 = interp(left, nv)?;
            let v2 = interp(right, nv)?;
            concat(&v1, &v2)
        },
        Exp::LessThan { left, right } => {
            let v1 = interp(left, nv)?;
            let v2 = interp(right, nv)?;
            less_than(&v1, &v2)
        }
        Exp::Cnd { tst, thn, els } => {
            let tst_v = interp(tst, nv)?;
            if boolean_decision(&tst_v)? {
                interp(thn, nv)
            } else {
                interp(els, nv)
            }
        }
        Exp::Let1 { var, value, body } => {
            let val = interp(value, nv)?;
            let mut new_env = nv.clone();
            // insert the value wrapped in Rc<RefCell<Option<Value>>>
            new_env.insert(var.clone(), Rc::new(RefCell::new(Some(val))));
            interp(body, &new_env)
        },
        Exp::Rec { var, value, body, .. } => {
            // initialize a cell with None value
            let cell = Rc::new(RefCell::new(None));
            let mut new_env = nv.clone();
            // insert the variable into the environment before evaluation
            new_env.insert(var.clone(), cell.clone());
            // evaluate the value in the new environment
            let val = interp(value, &new_env)?;
            // update the cell with the evaluated value
            *cell.borrow_mut() = Some(val);
            // evaluate the body in the new environment
            interp(body, &new_env)
        },
        Exp::Lam { var, var_type, body } => {
            Ok(Value::Fun {
                var: var.clone(),
                var_type: var_type.clone(),
                body: body.clone(),
                nv: nv.clone(),
            })
        },
        Exp::App { fun, arg } => {
            let fv = interp(fun, nv)?;
            let av = interp(arg, nv)?;
            match fv {
                Value::Fun { var, body, nv: fun_nv, .. } => {
                    let mut new_env = fun_nv.clone();
                    // insert the argument value into the function's environment
                    new_env.insert(var.clone(), Rc::new(RefCell::new(Some(av))));
                    interp(&body, &new_env)
                },
                _ => Err("Expected a function".to_string()),
            }
        },
    }
}

fn lookup(s: &str, env: &Env) -> Result<Value, String> {
    if let Some(cell) = env.get(s) {
        if let Some(val) = &*cell.borrow() {
            Ok(val.clone())
        } else {
            Err(format!("Variable {} is not yet initialized", s))
        }
    } else {
        Err(format!("{} not bound", s))
    }
}

fn add(v1: &Value, v2: &Value) -> Result<Value, String> {
    if let (Value::Int(n1), Value::Int(n2)) = (v1, v2) {
        Ok(Value::Int(n1 + n2))
    } else {
        Err(format!("+ expects two integers, got {:?} + {:?}", v1, v2))
    }
}

fn concat(v1: &Value, v2: &Value) -> Result<Value, String> {
    if let (Value::Str(s1), Value::Str(s2)) = (v1, v2) {
        Ok(Value::Str(format!("{}{}", s1, s2)))
    } else {
        Err(format!("+ expects two strings, got {:?} + {:?}", v1, v2))
    }
}

fn boolean_decision(v: &Value) -> Result<bool, String> {
    if let Value::Bool(b) = v {
        Ok(*b)
    } else {
        Err(format!("boolean expected, found {:?}", v))
    }
}

fn less_than(v1: &Value, v2: &Value) -> Result<Value, String> {
    if let (Value::Int(n1), Value::Int(n2)) = (v1, v2) {
        Ok(Value::Bool(n1 < n2))
    } else {
        Err(format!(
            "< expects two integers, got {:?} + {:?}",
            v1, v2
        ))
    }
}
