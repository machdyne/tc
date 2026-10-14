; Code as data: an evaluator for a tiny language of sums and
; products, and a lookup table kept as a list of pairs.

(define (calc e)
  (cond ((number? e) e)
        ((eq? (car e) '+) (+ (calc (cadr e)) (calc (caddr e))))
        ((eq? (car e) '*) (* (calc (cadr e)) (calc (caddr e))))
        (else 'unknown)))

(calc '(+ 1 (* 2 3)))         ; => 7

(define phones '((anna . 4711) (ben . 2501) (cleo . 1234)))
(cdr (assq 'ben phones))      ; => 2501

(check (calc '(+ 1 (* 2 3))) 7)
(check (calc '(* (+ 1 2) (+ 3 4))) 21)
(check (calc 5) 5)
(check (cdr (assq 'ben phones)) 2501)
(check (assq 'dora phones) #f)
