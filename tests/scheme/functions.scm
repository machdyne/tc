; Functions as values: map, a filter written by hand, lambda,
; and closures.

(define (square x) (* x x))

(map square '(1 2 3 4))       ; => (1 4 9 16)

(define (keep ok? lst)
  (cond ((null? lst) '())
        ((ok? (car lst)) (cons (car lst) (keep ok? (cdr lst))))
        (else (keep ok? (cdr lst)))))

(keep even? '(1 2 3 4 5 6))           ; => (2 4 6)
(keep (lambda (x) (> x 10)) '(5 50 8 80))   ; => (50 80)

(define (make-counter)
  (let ((count 0))
    (lambda ()
      (set! count (+ count 1))
      count)))

(define tally (make-counter))
(tally)                       ; => 1
(tally)                       ; => 2

(check (map square '(1 2 3 4)) '(1 4 9 16))
(check (keep even? '(1 2 3 4 5 6)) '(2 4 6))
(check (keep (lambda (x) (> x 10)) '(5 50 8 80)) '(50 80))
(define t2 (make-counter))
(check (t2) 1)
(check (t2) 2)
(check (t2) 3)
(define t3 (make-counter))
(check (t3) 1)
