; Numbers in Machdyne Scheme are doubles (Scheme).

(/ 7 2)                       ; => 3.5
(quotient 7 2)                ; => 3
(= (+ 0.1 0.2) 0.3)           ; => #f

(define (close? a b)
  (< (abs (- a b)) 0.000001))
(close? (+ 0.1 0.2) 0.3)      ; => #t

(check (/ 7 2) 3.5)
(check (quotient 7 2) 3)
(check (= (+ 0.1 0.2) 0.3) #f)
(check (close? (+ 0.1 0.2) 0.3) #t)
