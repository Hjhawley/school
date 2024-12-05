use super::*;

struct Sub {
    input_variable: String,
    output_term: Term,
}

fn apply_subs(subs: &Vec<Sub>, mut term: Term) -> Term {
    for Sub { input_variable, output_term } in subs {
        term = match term {
            Term::Var(name) if name == *input_variable => {
                output_term.clone()
            }
            Term::Compound { head_atom: atom_name, termlist: input_list } => {
                let head_atom = atom_name.clone();
                let mut termlist = Vec::new();
                for elt in input_list {
                    termlist.push(apply_subs(subs, elt));
                }
                Term::Compound { head_atom, termlist }
            }
            _ => term.clone()
        };
    }
    term
}

fn mgu(a: &Term, b: &Term) -> Result<Vec<Sub>, ()> {
    let mut unifier = Vec::new();
    let mut a_list = vec![a.clone()];
    let mut b_list = vec![b.clone()];
    while !a_list.is_empty() && !b_list.is_empty() {
        match (a_list.remove(0), b_list.remove(0)) {
            (output_term, Term::Var(input_variable)) => {
                // anything unifies with a variable
                unifier.push(Sub { input_variable, output_term });
                for term in std::mem::take(&mut a_list) {
                    a_list.push(apply_subs(&unifier, term));
                }
                for term in std::mem::take(&mut b_list) {
                    b_list.push(apply_subs(&unifier, term));
                }
            }
            (Term::Var(input_variable), output_term) => {
                // a variable unifies with anything
                unifier.push(Sub { input_variable, output_term });
                for term in std::mem::take(&mut a_list) {
                    a_list.push(apply_subs(&unifier, term));
                }
                for term in std::mem::take(&mut b_list) {
                    b_list.push(apply_subs(&unifier, term));
                }
            }
            (Term::Atom(a), Term::Atom(b)) => {
                // atoms must match
                if a != b {
                    return Err(())
                }
            }
            (Term::Compound{head_atom: head_a, termlist: lst_a}, Term::Compound{head_atom: head_b, termlist: lst_b}) => {
                if head_a != head_b || lst_a.len() != lst_b.len() {
                    return Err(());
                }
                a_list.extend_from_slice(&lst_a);
                b_list.extend_from_slice(&lst_b);
            }
            _ => return Err(()),
        }
    }
    Ok(unifier)
}

fn succeed(term: &Term) {
    println!("SUCCESS: {term}");
}

fn resolution(subs: &Vec<Sub>, clause: &Clause, goals: &Vec<Term>, query: &Term) -> (Vec<Term>, Term) {
    let mut new_goals = Vec::new();
    match clause {
        Clause::Fact(_) => {
            // If it's a fact, just use the tail of the goals
            new_goals.extend(goals.iter().skip(1).cloned());
        }
        Clause::Rule(_, body) => {
            // If it's a rule, append the body of the clause
            for term in body {
                new_goals.push(apply_subs(subs, term.clone()));
            }
            new_goals.extend(goals.iter().skip(1).map(|term| apply_subs(subs, term.clone())));
        }
    }

    let updated_query = apply_subs(subs, query.clone());

    (new_goals, updated_query)
}


pub fn solve(program: &Vec<Clause>, goals: &Vec<Term>, query: &Term) {
    if goals.is_empty() {
        succeed(query);
        return;
    }
    let current_goal = &goals[0];
    for clause in program {
        let clause_head = match clause {
            Clause::Fact(head) => head,
            Clause::Rule(head, _) => head,
        };
        if let Ok(subs) = mgu(clause_head, current_goal) {
            let (new_goals, new_query) = resolution(&subs, clause, goals, query);
            solve(program, &new_goals, &new_query);
        }
    }
}
