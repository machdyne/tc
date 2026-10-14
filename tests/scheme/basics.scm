; Expressions, definitions and choices.

(define (square x) (* x x))
(square 12)                   ; => 144

(define (size n)
  (cond ((< n 10) 'small)
        ((< n 100) 'medium)
        (else 'large)))
(size 42)                     ; => medium

(check (square 12) 144)
(check (+ 1 (* 2 3)) 7)
(check (size 42) 'medium)
(check (size 7) 'small)
(check (size 1000) 'large)
