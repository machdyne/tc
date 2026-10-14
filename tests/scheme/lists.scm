; Lists: cons, car, cdr, and recursion over them.

(define days '(mon tue wed thu fri))
(car days)                    ; => mon
(cdr days)                    ; => (tue wed thu fri)
(cons 'sun days)              ; => (sun mon tue wed thu fri)

(define (sum lst)
  (if (null? lst)
      0
      (+ (car lst) (sum (cdr lst)))))
(sum '(3 1 4 1 5))            ; => 14

(check (car days) 'mon)
(check (cdr days) '(tue wed thu fri))
(check (cons 'sun days) '(sun mon tue wed thu fri))
(check (length days) 5)
(check (sum '(3 1 4 1 5)) 14)
(check (sum '()) 0)
