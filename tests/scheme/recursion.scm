; Recursion, and tail calls that run in constant space.

(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))
(factorial 10)                ; => 3628800

(define (sum-to n)
  (let loop ((i 1) (total 0))
    (if (> i n)
        total
        (loop (+ i 1) (+ total i)))))
(sum-to 100)                  ; => 5050

(check (factorial 10) 3628800)
(check (sum-to 100) 5050)
; a million iterations: only possible if the tail call does not grow
; the stack
(check (sum-to 1000000) 500000500000)
