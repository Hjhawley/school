use super::*;

#[derive(Debug)]
struct Sub {
    input_variable: String,
    output_term: Term,
}

fn apply_subs(subs: &Vec<Sub>, term: Term) -> Term {
    match term {
        Term::Var(name) => {
            for Sub { input_variable, output_term } in subs {
                if &name == input_variable {
                    return apply_subs(subs, output_term.clone());
                }
            }
            Term::Var(name) // No substitution found
        }
        Term::Compound { head_atom, termlist } => Term::Compound {
            head_atom,
            termlist: termlist
                .into_iter()
                .map(|t| apply_subs(subs, t))
                .collect(),
        },
        _ => term, // Atoms remain unchanged
    }
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
                    return Err(());
                }
            }
            (
                Term::Compound { head_atom: head_a, termlist: lst_a },
                Term::Compound { head_atom: head_b, termlist: lst_b },
            ) => {
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
    println!("SUCCESS: {}", term);
}

fn resolution(subs: &Vec<Sub>, clause: &Clause, goals: &Vec<Term>, query: &Term) -> (Vec<Term>, Term) {
    let mut new_goals = Vec::new();
    match clause {
        Clause::Fact(_) => {
            new_goals.extend(goals.iter().skip(1).map(|g| apply_subs(subs, g.clone())));
        }
        Clause::Rule(_, body) => {
            new_goals.extend(body.iter().map(|b| apply_subs(subs, b.clone())));
            new_goals.extend(goals.iter().skip(1).map(|g| apply_subs(subs, g.clone())));
        }
    }
    let updated_query = apply_subs(subs, query.clone());
    (new_goals, updated_query)
}

pub fn solve(program: &Vec<Clause>, goals: &Vec<Term>, query: &Term) {
    fn solve_internal(
        program: &Vec<Clause>,
        goals: &Vec<Term>,
        query: &Term,
        visited: &mut Vec<Term>,
    ) {
        if goals.is_empty() {
            succeed(query);
            return;
        }
        let current_goal = &goals[0];
        // Prevent revisiting the same goal
        if visited.contains(current_goal) {
            return;
        }
        visited.push(current_goal.clone());
        for clause in program {
            let clause_head = match clause {
                Clause::Fact(head) => head,
                Clause::Rule(head, _) => head,
            };
            if let Ok(subs) = mgu(clause_head, current_goal) {
                let (new_goals, new_query) = resolution(&subs, clause, goals, query);
                solve_internal(program, &new_goals, &new_query, visited);
            }
        }
        visited.pop(); // Backtracking
    }
    let mut visited = Vec::new(); // Initialize the visited list
    solve_internal(program, goals, query, &mut visited);
}