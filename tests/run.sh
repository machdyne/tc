#!/bin/sh
#
# Run every example in the book.
#
#   basic/NAME.bas     fed to Machdyne BASIC, followed by RUN unless the
#                      file has its own; the output must match NAME.out.
#                      A line marked REM TEST is not in the book: it
#                      stops a program that would otherwise run for ever
#   scheme/NAME.scm    run by Machdyne Scheme after its standard library
#                      and scheme/check.scm; a failed (check ...) exits 1,
#                      and if NAME.out exists the output must match it
#   c/NAME.c           compiled as strict C99 and run; the output must
#                      match NAME.out (no NAME.out: compiled only)
#   asm/NAME.S         assembled as RV32I; if NAME.out exists, the machine
#                      code words must match it
#   verilog/tb_NAME.v  simulated with Icarus Verilog against NAME.v and
#                      must print PASS; NAME.v must also synthesise
#
# EXT is where `make deps` put the external projects. A language whose
# tools are missing is skipped with a note, not failed, so a partial
# setup still checks what it can.

here=$(cd "$(dirname "$0")" && pwd)
EXT=${EXT:-$here/../ext}
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

pass=0
fail=0
skip=0

ok()   { pass=$((pass + 1)); }
bad()  { fail=$((fail + 1)); echo "FAIL $1"; [ -n "$2" ] && sed 's/^/     /' "$2"; }
note() { skip=$((skip + 1)); echo "skip $1"; }

# -- BASIC --

basic="$EXT/basic/basic"
for src in "$here"/basic/*.bas; do
	[ -e "$src" ] || continue
	name=basic/$(basename "$src" .bas)
	[ -x "$basic" ] || { note "$name: no $basic (make deps)"; continue; }
	# The interpreter keeps files in its current directory.
	mkdir -p "$work/basic" && cd "$work/basic" && rm -f ./*
	# A test that needs commands after RUN (TYPE, say) has its own RUN.
	{ cat "$src"; grep -qx RUN "$src" || echo RUN; } |
		timeout 20 "$basic" 2>&1 |
		sed -e '/^\/\/\/$/d' -e 's/^\(> \)*//' -e '/^$/d' > "$work/out"
	if diff -u "${src%.bas}.out" "$work/out" > "$work/diff"; then
		ok
	else
		bad "$name" "$work/diff"
	fi
done

# -- Scheme --

ms="$EXT/ms/ms"
for src in "$here"/scheme/*.scm; do
	[ -e "$src" ] || continue
	name=scheme/$(basename "$src" .scm)
	[ "$(basename "$src")" = check.scm ] && continue
	[ -x "$ms" ] || { note "$name: no $ms (make deps)"; continue; }
	cat "$EXT/ms/ms_stdlib.l" "$here/scheme/check.scm" "$src" > "$work/t.scm"
	if ! "$ms" "$work/t.scm" > "$work/out" 2>&1 || grep -q '\[error\]' "$work/out"; then
		bad "$name" "$work/out"
	elif [ -f "${src%.scm}.out" ] && \
			! diff -u "${src%.scm}.out" "$work/out" > "$work/diff"; then
		bad "$name" "$work/diff"
	else
		ok
	fi
done

# -- C --

CC=${CC:-cc}
for src in "$here"/c/*.c; do
	[ -e "$src" ] || continue
	name=c/$(basename "$src" .c)
	if ! $CC -std=c99 -pedantic -Wall -Wextra -Werror -o "$work/a.out" \
			"$src" > "$work/err" 2>&1; then
		bad "$name" "$work/err"
		continue
	fi
	exp="${src%.c}.out"
	if [ ! -f "$exp" ]; then
		ok
		continue
	fi
	"$work/a.out" > "$work/out" 2>&1
	if diff -u "$exp" "$work/out" > "$work/diff"; then
		ok
	else
		bad "$name" "$work/diff"
	fi
done

# -- RISC-V assembly --

AS=${RISCV:-riscv64-unknown-elf-}as
OBJDUMP=${RISCV:-riscv64-unknown-elf-}objdump
for src in "$here"/asm/*.S; do
	[ -e "$src" ] || continue
	name=asm/$(basename "$src" .S)
	command -v "$AS" > /dev/null || { note "$name: no $AS"; continue; }
	if ! "$AS" -march=rv32i -mabi=ilp32 -o "$work/a.o" "$src" \
			> "$work/err" 2>&1; then
		bad "$name" "$work/err"
		continue
	fi
	exp="${src%.S}.out"
	if [ ! -f "$exp" ]; then
		ok
		continue
	fi
	# the machine code words, one per line
	"$OBJDUMP" -d "$work/a.o" |
		sed -n 's/^ *[0-9a-f]*:[[:space:]]*\([0-9a-f]\{8\}\).*/\1/p' > "$work/out"
	if diff -u "$exp" "$work/out" > "$work/diff"; then
		ok
	else
		bad "$name" "$work/diff"
	fi
done

# -- Verilog --

for tb in "$here"/verilog/tb_*.v; do
	[ -e "$tb" ] || continue
	base=$(basename "$tb" .v)
	dut="$here/verilog/${base#tb_}.v"
	name=verilog/${base#tb_}
	command -v iverilog > /dev/null || { note "$name: no iverilog"; continue; }
	if ! iverilog -g2005 -o "$work/sim" "$tb" "$dut" > "$work/out" 2>&1; then
		bad "$name" "$work/out"
		continue
	fi
	vvp -n "$work/sim" > "$work/out" 2>&1
	if ! grep -q '^PASS' "$work/out"; then
		bad "$name" "$work/out"
		continue
	fi
	if command -v yosys > /dev/null; then
		if ! yosys -q -p "read_verilog $dut; synth -auto-top" \
				> "$work/out" 2>&1; then
			bad "$name (synthesis)" "$work/out"
			continue
		fi
	fi
	ok
done

echo "tests: $pass passed, $fail failed, $skip skipped"
[ "$fail" = 0 ]
