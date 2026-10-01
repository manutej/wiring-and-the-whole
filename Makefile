.PHONY: verify witness e2 dogfood-grade dogfood-grade-toybank dogfood-grade-fineract-thin external-slice-check fetch-slice-dry-run pack-v0-check pulse-gate pulse-eval pipeline-io wiringmap-check wiringmap-stress

verify:
	@./scripts/verify.sh

pulse-gate:
	@./scripts/pulse_gate.sh

pulse-eval:
	@bash scripts/pulse_eval_functional.sh

pipeline-io:
	@bash scripts/pipeline_world_io.sh

dogfood-grade:
	@python3 scripts/grade_l1_questions.py

dogfood-grade-toybank:
	@python3 scripts/grade_l1_questions.py --questions docs/dogfood/L1-TOYBANK-QUESTIONS.json

dogfood-grade-fineract-thin:
	@python3 scripts/grade_l1_questions.py --questions docs/dogfood/L1-FINERACT-THIN-QUESTIONS.json

external-slice-check:
	@bash scripts/fineract_slice_check.sh

fetch-slice-dry-run:
	@bash scripts/fetch_fineract_slice.sh

wiringmap-stress:
	@bash scripts/wiringmap_stress.sh

wiringmap-check:
	@python3 -m pip install -q jsonschema
	@python3 scripts/validate_wiringmap.py
	@python3 scripts/extract_toybank_refs.py

pack-v0-check:
	@python3 scripts/build_l2_pack.py wiringmap/examples/toybank-accounts.v0.json
	@python3 scripts/reexpand_gate.py wiringmap/examples/toybank-accounts.v0.pack

witness:
	@python3 witness/run_witness.py

e2:
	@cd experiments && (test -f package-lock.json && npm ci --silent || npm install --silent)
	@cd experiments/e2-tokens && python3 e2_run.py
