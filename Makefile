.PHONY: verify witness e2 dogfood-grade

verify:
	@./scripts/verify.sh

dogfood-grade:
	@python3 scripts/grade_l1_questions.py

witness:
	@python3 witness/run_witness.py

e2:
	@cd experiments && (test -f package-lock.json && npm ci --silent || npm install --silent)
	@cd experiments/e2-tokens && python3 e2_run.py
