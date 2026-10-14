; The one procedure every Scheme test uses. (check expr expected)
; compares with equal? and stops the run with exit status 1 on the
; first mismatch, printing what it got.

(define (check got want)
  (if (equal? got want)
      #t
      (begin
        (display "check failed: got ")
        (display got)
        (display ", wanted ")
        (display want)
        (display "
")
        (exit 1))))
