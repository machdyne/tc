; Euclid's algorithm, for the side-by-side appendix.

(define (gcd-of a b)
  (if (= b 0)
      a
      (gcd-of b (remainder a b))))

(gcd-of 1071 462)             ; => 21

(check (gcd-of 1071 462) 21)
(check (gcd-of 17 5) 1)
