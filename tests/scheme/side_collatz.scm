; The Collatz sequence: steps from 27 down to 1.

(define (collatz n steps)
  (cond ((= n 1) steps)
        ((even? n) (collatz (/ n 2) (+ steps 1)))
        (else (collatz (+ (* 3 n) 1) (+ steps 1)))))

(collatz 27 0)                ; => 111

(check (collatz 27 0) 111)
(check (collatz 1 0) 0)
