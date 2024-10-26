Implementing functions
======================

Please refer to the “Evaluating Functions” section of the
“Evaluation” chapter in the book.

Your task is to update the interpreter to understand function
literals (lambda functions) and apply functions using syntax like
the following examples:

    fn(x) { x + 19 }(2)

    let double = fn(n) { n + n } { double(5 + 6) }

`main.rs` already contains the needed updates and you should not
change it. `parse.rs` is also updated to tokenize and parse the new
syntax and will not require modifications.

Start in `interp.rs` by copying your implementation for `Let1`
expressions.

Next, add implementations for function definition and application by
adapting the following version from the book:

    [(lamE v b) (funV v b nv)]

    [(appE f a) (let ([fv (interp f nv)]
                      [av (interp a nv)])
                  (type-case Value fv
                    [(funV v b nv)
                     (interp b (extend nv v av))]
                    [else (error 'app "didn't get a function")]))]
