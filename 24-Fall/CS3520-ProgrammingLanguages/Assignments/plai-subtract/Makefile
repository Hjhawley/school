.SUFFIXES:
.SUFFIXES: .rs .out .xml .lock

STEPPER_DELAY=0.01
STEPPER_WARMUPDELAY=0.1
STEPPER_POSTCRASHLINES=15
STEPPER_WRONGLINES=10
STEPPER_SUFFIX=input
STEPPER_INDIR=inputs
STEPPER_OUTDIR=inputs
STEPPER_CMD=target/debug/student
export STEPPER_DELAY STEPPER_WARMUPDELAY STEPPER_POSTCRASHLINES STEPPER_WRONGLINES
export STEPPER_SUFFIX STEPPER_INDIR STEPPER_OUTDIR STEPPER_CMD

all:	step

grade:	target/debug/student
	rm -f test_detail.xml inputs/*.actual
	python3 lib/grader

run:	target/debug/student
	target/debug/student

step:	target/debug/student
	python3 lib/stepper

target/debug/student:	src/*.rs Cargo.toml
	cargo build

setup:
	sudo apt install -y cargo icdiff make python3

clean:
	cargo clean
	rm -f *.lock *.xml
