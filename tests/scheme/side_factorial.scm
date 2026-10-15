; Factorial by recursion, for the side-by-side appendix.

(define (factorial n)
  (if (= n 0)
      1
      (* n (factorial (- n 1)))))

(factorial 7)                 ; => 5040

(check (factorial 7) 5040)
