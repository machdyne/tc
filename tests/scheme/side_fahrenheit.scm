; A conversion table, printed by a recursive procedure that counts up.
; The output is compared with side_fahrenheit.out.

(define (table c)
  (if (<= c 100)
      (begin
        (display c)
        (display " ")
        (display (+ (/ (* c 9) 5) 32))
        (display "\n")
        (table (+ c 20)))))

(table 0)
