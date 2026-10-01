.PHONY: verify witness e2 dogfood-grade pulse-gate wiringmap-check

verify:
	@./scripts/verify.sh

pulse-gate:
	@./scripts/pulse_gate.sh

dogfood-grade:
	@python3 scripts/grade_l1_questions.py

wiringmap-check:
	@python3 -m pip install -q jsonschema
	@python3 scripts/validate_wiringmap.py
	@python3 scripts/extract_toybank_refs.py

witness:
	@python3 witness/run_witness.py

e2:
	@cd experiments && (test -f package-lock.json && npm ci --silent || npm install --silent)
	@cd experiments/e2-tokens && python3 e2_run.py
